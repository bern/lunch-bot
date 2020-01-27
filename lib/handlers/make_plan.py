from datetime import datetime
from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.plan import Plan
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_make_plan(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    if len(args) != 3:
        common.send_reply(
            client,
            message,
            "Oops! The make-plan command requires more information. Type help for formatting instructions.",
        )
        return

    try:
        plan_time = common.parse_time(args[2])
    except ValueError as e:
        common.send_reply(
            client,
            message,
            "Sorry, the time you entered could not be used because it is not a valid date format.",
        )
        return

    now = common.get_now()
    if plan_time < now:
        common.send_reply(
            client,
            message,
            "Sorry, you can't plan for a lunch before the current time.",
        )
        return

    if not storage.contains(storage.PLANS_ENTRY):
        storage.put(storage.PLANS_ENTRY, {})

    plans = storage.get(storage.PLANS_ENTRY)
    for _, plan in plans.items():
        if plan.restaurant == args[1] and plan.time == plan_time:
            common.send_reply(
                client,
                message,
                "Sorry, there is already a plan with that name and time. How about you RSVP instead?",
            )
            return

    user = User.get_sender(message)
    plan = Plan(args[1], plan_time, [user])

    plans = storage.get(storage.PLANS_ENTRY)
    plans[plan.uuid] = plan
    storage.put(storage.PLANS_ENTRY, plans)

    common.send_reply(
        client,
        message,
        "I have added your plan! Enjoy lunch, {}!".format(user.full_name),
    )
