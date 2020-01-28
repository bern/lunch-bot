from datetime import datetime
from collections import defaultdict
import regex as re
from typing import Callable
from typing import Dict
from typing import Optional
from typing import List
import zulip

from lib.state_handler import StateHandler
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


def render_plan(plan: Plan, short: bool = False) -> str:
    """
    Standard function to render a Plan so that it's uniform across all handlers.
    """
    return "{} @ {}, {} RSVP{}".format(
        plan.restaurant,
        render_plan_time(plan),
        len(plan.rsvps),
        "s" if len(plan.rsvps) != 1 else "",
    )


def render_plan_short(plan: Plan) -> str:
    """
    Rendering a plan without the RSVP information.
    """
    return "{} @ {}".format(plan.restaurant, render_plan_time(plan))


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


def parse_time(date_str: str) -> datetime:
    """
    Parses out a string-formatted date into a well-structured datetime in UTC.
    Supports any of the following formats:

      - hh:mm

        In this format, we treat the value of the hh section to be 24hr format.
        If a user types in 1:00, it will be interpreted as 1am, not 1pm.

      - hh:mm(am|pm)

        In this format, we treat the value of the hh section to be 12hr format,
        and we rely on the am/pm flag to determine whether it is in the morning
        or the afternoon.
    """
    match = re.match(r"(\d?\d):(\d\d)(am|pm)?", date_str)
    if match is None:
        raise ValueError()

    groups = match.groups()
    hour = int(groups[0])
    minute = int(groups[1])
    if groups[2] == "pm" and hour < 12:
        hour += 12

    now = get_now()
    time = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )

    return time


def get_matching_plans(
    restaurant: str, storage: StateHandler, time: Optional[datetime] = None,
) -> List[Plan]:
    """
    Returns a list of matching plans, given a restaurant name and an optional time.
    """
    matching_plans = []
    plans = storage.get(StateHandler.PLANS_ENTRY)

    for _, plan in plans.items():
        if plan.restaurant == restaurant and (time is None or plan.time == time):
            matching_plans.append(plan)
    return matching_plans
