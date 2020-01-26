from datetime import datetime
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
                recipient["email"]
                for recipient in message["display_recipient"]
                if client.email != recipient["email"]
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
