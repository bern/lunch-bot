from typing import Any
from typing import Dict
from typing import Callable
import zulip

from lib import state_handler
from lib.handlers import HandlerParams
from lib.handlers.alert_leaving import handle_alert_leaving
from lib.handlers.delete_plan import handle_delete_plan
from lib.handlers.help import handle_help
from lib.handlers.make_plan import handle_make_plan
from lib.handlers.my_plans import handle_my_plans
from lib.handlers.not_a_command import handle_not_a_command
from lib.handlers.reset import handle_reset
from lib.handlers.rsvp import handle_rsvp
from lib.handlers.show_plans import handle_show_plans
from lib.handlers.un_rsvp import handle_un_rsvp
from lib.models.message import Message


class LunchBotHandler(object):
    """
    Let's get lunch!
    """

    def __init__(self, client: zulip.Client, storage: state_handler.StateHandler):
        self.client = client
        self.storage = storage

        self.default_handler: Callable[[HandlerParams], None] = handle_not_a_command
        self.handlers: Dict[str, Callable[[HandlerParams], None]] = {
            "alert-leaving": handle_alert_leaving,
            "delete-plan": handle_delete_plan,
            "help": handle_help,
            "make-plan": handle_make_plan,
            "my-plans": handle_my_plans,
            "reset": handle_reset,
            "rsvp": handle_rsvp,
            "show-plans": handle_show_plans,
            "un-rsvp": handle_un_rsvp,
        }

    def usage(self):
        return """
        lunch-bot is a bot that helps Recursers organize groups to get lunch! Type help to get started.
        """

    def safe_handle_message(self, message: Dict[str, Any]):
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

    def handle_message(self, message: Dict[str, Any]):
        """
        Handles messages from users on Zulip. Handles the provided command, and
        responds with the appropriate message.

        Delegates responsibilities to handlers defined in lib.handlers.*
        """
        # If the bot was the sender of the message, then skip processing the
        # message.
        parsed_message = Message.parse_zulip_message(message)
        args = parsed_message.content.split()
        if parsed_message.sender_email == self.client.email or len(args) == 0:
            return

        self.handlers.get(args[0], self.default_handler)(
            HandlerParams(
                args=args,
                client=self.client,
                message=parsed_message,
                storage=self.storage,
            ),
        )
