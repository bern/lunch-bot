from typing import List
import zulip

from lib import common
from lib.handlers import HandlerParams
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_reset(params: HandlerParams):
    if len(params.args) == 2 and params.args[1] == "confirm":
        params.storage.put(params.storage.PLANS_ENTRY, {})
        return

    common.send_reply(
        params.client,
        params.message,
        "This will wipe all current lunches from my records. If you wish to continue, please type 'reset confirm'.",
    )
