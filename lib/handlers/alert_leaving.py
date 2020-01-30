import zulip

from lib import common
from lib.handlers import HandlerParams
from lib.models.plan import Plan


def handle_alert_leaving(params: HandlerParams):
    """
    Alerts members of a plan about when their plan is going to leave.
    """
    if len(params.args) < 2 or len(params.args) > 3:
        common.send_reply(
            params.client,
            params.message,
            "Oops! The alert-leaving command requires 1 or 2 arguments. Type"
            " help for formatting instructions.",
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
            "There are no existing plans. Why not create one?",
        )
        return

    matching_plans = common.get_matching_plans(
        params.args[1], params.storage, time=time
    )

    if len(matching_plans) == 0:
        common.send_reply(
            params.client,
            params.message,
            "That lunch_id doesn't exist! Type show-plans to see each lunch_id"
            " and its associated lunch plan.",
        )
        return

    if len(matching_plans) > 1:
        common.send_reply(
            params.client,
            params.message,
            "There are multiple lunches with that lunch_id. Please reissue the"
            " command with the time of the lunch you're interested in:\n"
            "{}".format(
                "\n".join([common.render_plan_short(plan) for plan in matching_plans]),
            ),
        )
        return

    alert_leaving(params.client, matching_plans[0])


def alert_leaving(client: zulip.Client, plan: Plan):
    """
    Controller for alert_leaving. Executes if everything else goes well.
    """
    now = common.get_now()
    client.send_message(
        {
            "type": "private",
            "to": [user.email for user in plan.rsvps],
            "content": "Heads up! You're going to {} in {}".format(
                plan.restaurant, str(plan.time - now),
            ),
        }
    )
