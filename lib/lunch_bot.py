from typing import Any
from typing import Dict
import zulip

from lib import state_handler
from lib.handlers.delete_plan import DeletePlanHandler
from lib.handlers.help import HelpHandler
from lib.handlers.make_plan import MakePlanHandler
from lib.handlers.my_plans import MyPlansHandler
from lib.handlers.rsvp import RsvpHandler
from lib.handlers.show_plans import ShowPlansHandler
from lib.handlers.un_rsvp import UnRsvpHandler


class LunchBotHandler(object):
    """
    Let's get lunch!
    """

    def __init__(self, client: zulip.Client, storage: state_handler.StateHandler):
        self.client = client
        self.storage = storage

        self.handlers = {
            "delete-plan": DeletePlanHandler(),
            "help": HelpHandler(),
            "make-plan": MakePlanHandler(),
            "my-plans": MyPlansHandler(),
            "rsvp": RsvpHandler(),
            "show-plans": ShowPlansHandler(),
            "un-rsvp": UnRsvpHandler(),
        }

    def usage(self):
        return """
        lunch-bot is a bot that helps Recursers organize groups to get lunch! Type help to get started.
        """

    def handle_message(self, message):
        # By default, self.storage accepts any object for keys and values,
        # as long as it is JSON-able. Internally, the object then gets converted
        # to a UTF-8 string.

        # If the bot was the sender of the message, then skip processing the
        # message.
        # print(self.client.get_profile({"user_id": message["sender_id"]}))
        if message["sender_email"] == self.client.email:
            return

        # Given message is an object
        if message["content"] == "reset":
            self.send_reply(
                message,
                'This will wipe all current lunches from my records. If you wish to continue, please type "reset confirm".',
            )
            return

        if message["content"] == "reset confirm":
            self.storage.put("lunches", [])
            return

        message_args = message["content"].split()

        if len(message_args) == 0:
            self.send_reply(
                message,
                "Oops! You need to provide a lunch-bot command! Type help for a list of commands I understand :-)",
            )
            return

        if not message_args[0] in self.handlers:
            self.send_reply(
                message,
                "Oops! {} is not a valid lunch-bot command! Type help for a list of commands I understand :-)".format(
                    message_args[0]
                ),
            )

        self.handlers[message_args[0]].handle_message(
            self.client, self.storage, message, message_args,
        )

