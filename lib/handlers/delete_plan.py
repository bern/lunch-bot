from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_delete_plan(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    if len(args) != 2:
        common.send_reply(
            client,
            message,
            "Oops! The delete-plan command requires more information. Type help for formatting instructions.",
        )
        return

    # TODO: Replace occurrences of "lunches" with a constant value that
    #       defines the name of the lunches/plans table.
    if not storage.contains("lunches") or len(storage.get("lunches")) == 0:
        common.send_reply(
            client,
            message,
            "There are no lunch plans to delete! Why not add one using the make-plan command?",
        )
        return

    try:
        plan_id = int(args[1])
    except ValueError:
        common.send_reply(
            client,
            message,
            "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    plans = storage.get("lunches")
    if plan_id >= len(plans) or plan_id < 0:
        common.send_reply(
            client,
            message,
            "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    del plans[plan_id]
    storage.put("lunches", plans)

    common.send_reply(
        client, message, "You've successfully deleted lunch {}.".format(plan_id)
    )
