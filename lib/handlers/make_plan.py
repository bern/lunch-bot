from datetime import datetime
from typing import List
import zulip

from lib import common
from lib.handlers import HandlerParams
from lib.models.message import Message
from lib.models.plan import Plan
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_make_plan(params: HandlerParams):
    if len(params.args) != 3:
        common.send_reply(
            params.client,
            params.message,
            "Oops! The make-plan command requires more information. Type help for formatting instructions.",
        )
        return

    try:
        plan_time = common.parse_time(params.args[2])
    except ValueError as e:
        common.send_reply(
            params.client,
            params.message,
            "Sorry, the time you entered could not be used because it is not a valid date format.",
        )
        return

    now = common.get_now()
    if plan_time < now:
        common.send_reply(
            params.client,
            params.message,
            "Sorry, you can't plan for a lunch before the current time.",
        )
        return

    if not params.storage.contains(params.storage.PLANS_ENTRY):
        params.storage.put(params.storage.PLANS_ENTRY, {})

    plans = params.storage.get(params.storage.PLANS_ENTRY)
    for _, plan in plans.items():
        if plan.restaurant == params.args[1] and plan.time == plan_time:
            common.send_reply(
                params.client,
                params.message,
                "Sorry, there is already a plan with that name and time. How about you RSVP instead?",
            )
            return

    user = User.get_sender(params.message)
    plan = Plan(params.args[1], plan_time, [user])

    plans = params.storage.get(params.storage.PLANS_ENTRY)
    plans[plan.uuid] = plan
    params.storage.put(params.storage.PLANS_ENTRY, plans)

    common.send_reply(
        params.client,
        params.message,
        "I have added your plan! Enjoy lunch, {}!".format(user.full_name),
    )
