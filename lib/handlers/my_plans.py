from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_my_plans(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    if not storage.contains("lunches") or len(storage.get("lunches")) == 0:
        common.send_reply(
            message,
            "There are no active lunch plans right now! Why not add one using the make-plan command?",
        )
        return

    user = User.get_sender(message)
    common.send_reply(
        client,
        message,
        "Here are the lunches you've RSVP'd to:\n{}".format(
            "\n".join(
                [
                    "{}: {} @ {}, {} RSVP(s)".format(
                        i, plan.restaurant, plan.time, len(plan.rsvps),
                    )
                    for i, plan in enumerate(storage.get("lunches"))
                    if user in plan.rsvps
                ]
            )
        ),
    )
