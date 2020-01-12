from typing import List
import zulip

from lib.handlers.base_handler import BaseHandler
from lib.handlers.base_handler import Message
from lib.models.message import Message
from lib.models.plan import Plan
from lib.models.user import User
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

        # TODO: Do validation on date, so that we can infer the time from the
        #       date input. With that information, send out reminders some time
        #       before folks leave for lunch.
        user = User.get_sender(message)
        plan = Plan(args[1], args[2], [user])

        if not storage.contains("lunches"):
            storage.put("lunches", [])

        lunch_list = storage.get("lunches")
        lunch_list.append(plan)
        storage.put("lunches", lunch_list)

        self.send_reply(
            client,
            message,
            "I have added your plan! Enjoy lunch, {}!".format(user.full_name),
        )
