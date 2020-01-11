from typing import List
import zulip

from lib.handlers.base_handler import BaseHandler
from lib.handlers.base_handler import Message
from lib.state_handler import StateHandler


class MakePlanHandler(BaseHandler):
    def handle_message(
        self,
        client: zulip.Client,
        storage: StateHandler,
        message: Message,
        args: List[str],
    ):
        if len(args) != 3:
            self.send_reply(
                client,
                message,
                "Oops! The make-plan command requires more information. Type help for formatting instructions.",
            )
            return

        plan = {
            "restaurant": args[1],
            "time": args[2],
            "rsvps": message["display_recipient"],
        }

        if not storage.contains("lunches"):
            storage.put("lunches", [])

        lunch_list = storage.get("lunches")
        lunch_list.append(plan)
        storage.put("lunches", lunch_list)

        self.send_reply(
            client,
            message,
            "I have added your plan! Enjoy lunch, {}!".format(
                message["display_recipient"]
            ),
        )
