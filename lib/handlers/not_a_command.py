from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_not_a_command(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    common.send_reply(
        client,
        message,
        "Oops! '{}' is not a valid lunch-bot command! Type help for a list of commands I understand :-)".format(
            args[0],
        ),
    )
