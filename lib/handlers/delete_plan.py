from lib import common
from lib.controllers.delete_plan import delete_plan
from lib.handlers import HandlerParams


def handle_delete_plan(params: HandlerParams,):
    if len(params.args) < 2 or len(params.args) > 3:
        common.send_reply(
            params.client,
            params.message,
            "Oops! The delete-plan command requires more information. Type help for formatting instructions.",
        )
        return

    time = None
    if len(params.args) == 3:
        time = common.parse_time(params.args[2])

    if (
        not params.storage.contains(params.storage.PLANS_ENTRY)
        or len(params.storage.get(params.storage.PLANS_ENTRY)) == 0
    ):
        common.send_reply(
            params.client,
            params.message,
            "There are no lunch plans to delete! Why not add one using the make-plan command?",
        )
        return

    matching_plans = common.get_matching_plans(
        params.args[1], params.storage, time=time
    )

    if len(matching_plans) == 0:
        common.send_reply(
            params.client,
            params.message,
            "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
        )
        return

    if len(matching_plans) > 1:
        common.send_reply(
            params.client,
            params.message,
            "There are multiple lunches with that lunch_id. Please reissue the command with the time of the lunch"
            " you're interested in:\n{}".format(
                "\n".join([common.render_plan_short(plan) for plan in matching_plans]),
            ),
        )
        return

    plan = matching_plans[0]
    delete_plan(
        params.client, params.storage, plan,
    )
    params.cron.remove_event(plan.uuid)
    common.send_reply(
        params.client,
        params.message,
        "You've successfully deleted lunch {}.".format(common.render_plan_short(plan)),
    )
