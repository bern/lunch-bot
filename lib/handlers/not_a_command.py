from typing import List
import zulip

from lib.handlers.base_handler import BaseHandler
from lib.handlers.base_handler import Message
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


class NotACommandHandler(BaseHandler):
    def handle_message(
        self,
        client: zulip.Client,
        storage: StateHandler,
        message: Message,
        args: List[str],
    ):
        self.send_reply(
            client,
            message,
            "Oops! '{}' is not a valid lunch-bot command! Type help for a list of commands I understand :-)".format(
                args[0],
            ),
        )
