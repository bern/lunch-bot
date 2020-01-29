from typing import List
import zulip

from lib import common
from lib.handlers import HandlerParams
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_not_a_command(params: HandlerParams):
    common.send_reply(
        params.client,
        params.message,
        "Oops! '{}' is not a valid lunch-bot command! Type help for a list of commands I understand :-)".format(
            params.args[0],
        ),
    )
