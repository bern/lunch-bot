from lib import common
from lib.handlers import HandlerParams
from lib.models.user import User


def handle_my_plans(params: HandlerParams):
    if (
        not params.storage.contains(params.storage.PLANS_ENTRY)
        or len(params.storage.get(params.storage.PLANS_ENTRY)) == 0
    ):
        common.send_reply(
            params.client,
            params.message,
            "There are no active lunch plans right now! Why not add one using the make-plan command?",
        )
        return

    plans = params.storage.get(params.storage.PLANS_ENTRY)
    user = User.get_sender(params.message)
    common.send_reply(
        params.client,
        params.message,
        "Here are the lunches you've RSVP'd to:\n{}".format(
            "\n".join(
                [
                    common.render_plan(plan)
                    for _, plan in plans.items()
                    if user in plan.rsvps
                ]
            )
        ),
    )
