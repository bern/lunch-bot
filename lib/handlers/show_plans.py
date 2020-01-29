from typing import List
import zulip

from lib import common
from lib.handlers import HandlerParams
from lib.models.message import Message
from lib.state_handler import StateHandler


def handle_show_plans(params: HandlerParams):
    if (
        not params.storage.contains(params.storage.PLANS_ENTRY)
        or len(params.storage.get(params.storage.PLANS_ENTRY)) == 0
    ):
        common.send_reply(
            params.client,
            params.message,
            "There are no lunch plans to show! Why not add one using the make-plan command?",
        )
        return

    plans = params.storage.get(params.storage.PLANS_ENTRY)
    common.send_reply(
        params.client,
        params.message,
        "\n".join([common.render_plan(plan) for _, plan in plans.items()]),
    )
