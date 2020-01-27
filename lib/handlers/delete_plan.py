from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_delete_plan(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    if len(args) < 2 or len(args) > 3:
        common.send_reply(
            client,
            message,
            "Oops! The delete-plan command requires more information. Type help for formatting instructions.",
        )
        return

    use_time = False
    if len(args) == 3:
        use_time = True
        time = common.parse_time(args[2])

    if (
        not storage.contains(storage.PLANS_ENTRY)
        or len(storage.get(storage.PLANS_ENTRY)) == 0
    ):
        common.send_reply(
            client,
            message,
            "There are no lunch plans to delete! Why not add one using the make-plan command?",
        )
        return

    plans = storage.get(storage.PLANS_ENTRY)
    possible_plans = []
    for _, plan in plans.items():
        if plan.restaurant == args[1] and (not use_time or plan.time == time):
            possible_plans.append(plan)

    if len(possible_plans) == 0:
        common.send_reply(
            client,
            message,
            "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    if len(possible_plans) > 1:
        common.send_reply(
            client,
            message,
            "There are multiple lunches with that lunch_id. Please reissue the command with the time of the lunch you're interested in:\n{}".format(
                "\n".join([common.render_plan_short(plan) for plan in possible_plans]),
            ),
        )
        return

    plan = possible_plans[0]
    del plans[plan.uuid]
    storage.put(storage.PLANS_ENTRY, plans)

    common.send_reply(
        client,
        message,
        "You've successfully deleted lunch {}.".format(common.render_plan_short(plan),),
    )
