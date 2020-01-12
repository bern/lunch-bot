from typing import Any
from typing import Dict
import zulip

from lib import state_handler
from lib.handlers.delete_plan import DeletePlanHandler
from lib.handlers.help import HelpHandler
from lib.handlers.make_plan import MakePlanHandler
from lib.handlers.my_plans import MyPlansHandler
from lib.handlers.not_a_command import NotACommandHandler
from lib.handlers.reset import ResetHandler
from lib.handlers.rsvp import RsvpHandler
from lib.handlers.show_plans import ShowPlansHandler
from lib.handlers.un_rsvp import UnRsvpHandler
from lib.models.message import Message


class LunchBotHandler(object):
    """
    Let's get lunch!
    """

    def __init__(self, client: zulip.Client, storage: state_handler.StateHandler):
        self.client = client
        self.storage = storage

        self.default_handler = NotACommandHandler()
        self.handlers = {
            "delete-plan": DeletePlanHandler(),
            "help": HelpHandler(),
            "make-plan": MakePlanHandler(),
            "my-plans": MyPlansHandler(),
            "reset": ResetHandler(),
            "rsvp": RsvpHandler(),
            "show-plans": ShowPlansHandler(),
            "un-rsvp": UnRsvpHandler(),
        }

    def usage(self):
        return """
        lunch-bot is a bot that helps Recursers organize groups to get lunch! Type help to get started.
        """

    def safe_handle_message(self, message: Message):
        """
        A safe wrapper around handle_message that logs all errors, instead of
        crashing the bot. Useful for running in production where bugs aren't a
        problem, they're just log entries!
        """
        try:
            self.handle_message(message)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print(e)

    def handle_message(self, message: Message):
        """
        Handles messages from users on Zulip. Handles the provided command, and
        responds with the appropriate message.

        Delegates responsibilities to handlers defined in lib.handlers.*
        """
        # If the bot was the sender of the message, then skip processing the
        # message.
        args = message["content"].split()
        if message["sender_email"] == self.client.email or len(args) == 0:
            return

        self.handlers.get(args[0], self.default_handler).handle_message(
            self.client, self.storage, message, args
        )

