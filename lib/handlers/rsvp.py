from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_rsvp(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    if len(args) != 2:
        common.send_reply(
            client,
            message,
            "Oops! The rsvp command requires more information. Type help for formatting instructions.",
        )
        return

    if (
        not storage.contains(storage.PLANS_ENTRY)
        or len(storage.get(storage.PLANS_ENTRY)) == 0
    ):
        common.send_reply(
            message,
            "There are no lunch plans to RSVP to! Why not add one using the make-plan command?",
        )
        return

    try:
        rsvp_id = int(args[1])
    except ValueError:
        common.send_reply(
            client,
            message,
            "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    plans = storage.get(storage.PLANS_ENTRY)
    if rsvp_id >= len(plans) or rsvp_id < 0:
        common.send_reply(
            client,
            message,
            "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    user = User.get_sender(message)
    selected_plan = plans[rsvp_id]

    if user in selected_plan.rsvps:
        common.send_reply(
            client,
            message,
            "You've already RSVP'd to this lunch_id! Type my-plans to show all of your current lunch plans.",
        )
        return

    selected_plan.rsvps.append(user)
    plans[rsvp_id] = selected_plan
    storage.put(storage.PLANS_ENTRY, plans)

    common.send_reply(
        client,
        message,
        "Thanks for RSVPing to lunch  at {}! Enjoy your food, {}!".format(
            selected_plan.restaurant, user.full_name,
        ),
    )
