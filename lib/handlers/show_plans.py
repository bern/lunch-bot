from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.state_handler import StateHandler


def handle_show_plans(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str]
):
    if (
        not storage.contains(storage.PLANS_ENTRY)
        or len(storage.get(storage.PLANS_ENTRY)) == 0
    ):
        common.send_reply(
            client,
            message,
            "There are no lunch plans to show! Why not add one using the make-plan command?",
        )
        return

    common.send_reply(
        client,
        message,
        "\n".join(
            [
                "{}: {} @ {}, {} RSVP(s)".format(
                    i, plan.restaurant, common.render_plan_time(plan), len(plan.rsvps)
                )
                for i, plan in enumerate(storage.get(storage.PLANS_ENTRY))
            ]
        ),
    )
