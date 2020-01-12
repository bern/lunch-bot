from typing import List
import zulip

from lib.handlers.base_handler import BaseHandler
from lib.handlers.base_handler import Message
from lib.models.message import Message
from lib.models.user import User
from lib.state_handler import StateHandler


class ResetHandler(BaseHandler):
    def handle_message(
        self,
        client: zulip.Client,
        storage: StateHandler,
        message: Message,
        args: List[str],
    ):
        if len(args) == 2 and args[1] == "confirm":
            storage.put("lunches", [])
            return

        self.send_reply(
            client,
            message,
            "This will wipe all current lunches from my records. If you wish to continue, please type 'reset confirm'.",
        )
