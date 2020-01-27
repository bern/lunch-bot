from datetime import datetime
from collections import defaultdict
from typing import Callable
from typing import Dict
import zulip

from lib.models.message import Message
from lib.models.plan import Plan


def send_reply(client: zulip.Client, message: Message, reply: str):
    """
    Given an message object, send a string reply. Uses the metadata from
    the original message to determine to whom the response should be
    addressed.
    """
    client.send_message(
        {
            "type": "private",
            "to": [
                recipient.email
                for recipient in message.display_recipient
                if client.email != recipient.email
            ],
            "content": reply,
        }
    )


def render_plan_time(plan: Plan) -> str:
    """
    Renders the time of a plan as we would want it to appear to the user.
    """
    return plan.time.strftime("%I:%M%p").lower()


def get_now() -> datetime:
    """
    Returns the current time. Exactly equivalent to datetime.now(). This
    function only exists because it can be mocked, but datetime.now() cannot.
    """
    return datetime.now()


def min_edit_distance(
    source: str,
    target: str,
    insert_cost: Callable[[str], int] = lambda char: 1,
    delete_cost: Callable[[str], int] = lambda char: 1,
    replace_cost: Callable[[str, str], int] = lambda source_char, target_char: 0
    if source_char == target_char
    else 2,
) -> int:
    """
    Returns the minimum edit distance from between two strings. Allows the user
    to customize the functions used to calculate insert, delete, and replacement
    costs.
    """
    costs: Dict[int, Dict[int, int]] = defaultdict(lambda: defaultdict(lambda: 0))

    for i in range(len(source)):
        costs[i + 1][0] = costs[i][0] + delete_cost(source[i])
    for j in range(len(target)):
        costs[0][j + 1] = costs[0][j] + insert_cost(target[j])

    for j, target_char in enumerate(target):
        for i, source_char in enumerate(source):
            costs[i + 1][j + 1] = min(
                costs[i][j + 1] + delete_cost(target_char),
                costs[i + 1][j] + insert_cost(source_char),
                costs[i][j] + replace_cost(source_char, target_char),
            )
    return costs[len(source)][len(target)]
