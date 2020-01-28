from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_rsvp(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    if len(args) < 2 or len(args) > 3:
        common.send_reply(
            client,
            message,
            "Oops! The rsvp command requires more information. Type help for formatting instructions.",
        )
        return

    time = None
    if len(args) == 3:
        time = common.parse_time(args[2])

    if (
        not storage.contains(storage.PLANS_ENTRY)
        or len(storage.get(storage.PLANS_ENTRY)) == 0
    ):
        common.send_reply(
            client,
            message,
            "There are no lunch plans to RSVP to! Why not add one using the make-plan command?",
        )
        return

    plans = storage.get(storage.PLANS_ENTRY)
    matching_plans = common.get_matching_plans(args[1], storage, time=time)

    if len(matching_plans) == 0:
        common.send_reply(
            client,
            message,
            "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    if len(matching_plans) > 1:
        common.send_reply(
            client,
            message,
            "There are multiple lunches with that lunch_id. Please reissue the command with the time of the lunch you're interested in:\n{}".format(
                "\n".join([common.render_plan_short(plan) for plan in matching_plans]),
            ),
        )
        return

    user = User.get_sender(message)
    selected_plan = matching_plans[0]

    if user in selected_plan.rsvps:
        common.send_reply(
            client,
            message,
            "You've already RSVP'd to this lunch_id! Type my-plans to show all of your current lunch plans.",
        )
        return

    selected_plan.rsvps.append(user)
    plans[selected_plan.uuid] = selected_plan
    storage.put(storage.PLANS_ENTRY, plans)

    common.send_reply(
        client,
        message,
        "Thanks for RSVPing to lunch  at {}! Enjoy your food, {}!".format(
            selected_plan.restaurant, user.full_name,
        ),
    )
