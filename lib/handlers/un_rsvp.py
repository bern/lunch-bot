from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_un_rsvp(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    if len(args) != 2:
        common.send_reply(
            client,
            message,
            "Oops! The un-rsvp command requires more information. Type help for formatting instructions.",
        )
        return

    if not storage.contains("lunches") or len(storage.get("lunches")) == 0:
        common.send_reply(
            client,
            message,
            "There are no lunch plans to remove your RSVP from! Why not add one using the make-plan command?",
        )
        return

    # TODO: Change interface from numeric ID to a string ID. Maybe try to
    #       think about the UX surrounding plans.
    try:
        rsvp_id = int(args[1])
    except ValueError:
        common.send_reply(
            client,
            message,
            "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    plans = storage.get("lunches")
    if rsvp_id >= len(plans) or rsvp_id < 0:
        common.send_reply(
            client,
            message,
            "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    user = User.get_sender(message)
    selected_plan = plans[rsvp_id]

    if not user in selected_plan.rsvps:
        common.send_reply(
            client, message, "Oops! It looks like you haven't RSVP'd to this lunch_id!",
        )
        return

    selected_plan.rsvps.remove(user)
    plans[rsvp_id] = selected_plan
    storage.put("lunches", plans)

    common.send_reply(
        client,
        message,
        "You've successful un-RSVP'd to lunch at {}.".format(selected_plan.restaurant),
    )
