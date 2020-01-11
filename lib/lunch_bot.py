from typing import Any
from typing import Dict
import zulip

from lib import state_handler
from lib.handlers import delete_plan
from lib.handlers import help
from lib.handlers import make_plan
from lib.handlers import my_plans
from lib.handlers import rsvp
from lib.handlers import show_plans
from lib.handlers import un_rsvp


class LunchBotHandler(object):
    """
    Let's get lunch!
    """

    def __init__(self, client: zulip.Client, storage: state_handler.StateHandler):
        self.client = client
        self.storage = storage

    def usage(self):
        return """
        lunch-bot is a bot that helps Recursers organize groups to get lunch! Type help to get started.
        """

    def handle_message(self, message):
        # add your code here

        # bot_handler.send_message(dict(
        #     type='stream', # can be 'stream' or 'private'
        #     to=stream_name, # either the stream name or user's email
        #     subject=subject, # message subject
        #     content=message, # content of the sent message
        # ))

        # self.storage.put("foo", "bar")  # set entry "foo" to "bar"
        # print(self.storage.get("foo"))  # print "bar"
        # self.storage.contains("foo")

        # By default, self.storage accepts any object for keys and values,
        # as long as it is JSON-able. Internally, the object then gets converted
        # to a UTF-8 string.

        # If the bot was the sender of the message, then skip processing the
        # message.
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

        if not self.is_valid_command(message_args[0]):
            self.send_reply(
                message,
                "Oops! {} is not a valid lunch-bot command! Type help for a list of commands I understand :-)".format(
                    message_args[0]
                ),
            )

        if message_args[0] == "help":
            self.send_reply(
                message,
                help.run(),
            )

        if message_args[0] == "make-plan":
            # less than two arguments (doesnt have message_args[1] or message_args[2])
            if len(message_args) < 3:
                self.send_reply(
                    message,
                    "Oops! The make-plan command requires more information. Type help for formatting instructions.",
                )
                return

            plan = {
                "restaurant": message_args[1],
                "time": message_args[2],
                "rsvps": [message["display_recipient"]],
            }

            if not (self.storage.contains("lunches")):
                self.storage.put("lunches", [plan])
            else:
                lunch_list = self.storage.get("lunches")
                lunch_list.append(plan)
                self.storage.put("lunches", lunch_list)
            self.send_reply(
                message,
                "I have added your plan! Enjoy lunch, {}!".format(
                    message["display_recipient"]
                ),
            )

        if message_args[0] == "show-plans":
            if (
                not (self.storage.contains("lunches"))
                or len(self.storage.get("lunches")) == 0
            ):
                self.send_reply(
                    message,
                    "There are no lunch plans to show! Why not add one using the make-plan command?",
                )
            else:
                reply = ""
                lunches = self.storage.get("lunches")
                for i, lunch in enumerate(lunches):
                    reply += (
                        str(i)
                        + ": "
                        + lunch["restaurant"]
                        + " @ "
                        + lunch["time"]
                        + ", "
                        + str(len(lunch["rsvps"]))
                        + " RSVP(s)\n"
                    )

                reply = reply.rstrip()
                self.send_reply(message, reply)

        if message_args[0] == "my-plans":
            if (
                not (self.storage.contains("lunches"))
                or len(self.storage.get("lunches")) == 0
            ):
                self.send_reply(
                    message,
                    "There are no active lunch plans right now! Why not add one using the make-plan command?",
                )
            else:
                current_user = message["display_recipient"]

                reply = "Here are the lunches you've RSVP'd to:\n"
                lunch_list = self.storage.get("lunches")
                for i, lunch in enumerate(lunch_list):
                    if current_user in lunch["rsvps"]:
                        reply += (
                            str(i)
                            + ": "
                            + lunch["restaurant"]
                            + " @ "
                            + lunch["time"]
                            + ", "
                            + str(len(lunch["rsvps"]))
                            + " RSVP(s)\n"
                        )

                reply = reply.rstrip()
                self.send_reply(message, reply)

        if message_args[0] == "rsvp":
            # less than one arguments (doesnt have message_args[1])
            if len(message_args) < 2:
                self.send_reply(
                    message,
                    "Oops! The rsvp command requires more information. Type help for formatting instructions.",
                )
                return

            if (
                not (self.storage.contains("lunches"))
                or len(self.storage.get("lunches")) == 0
            ):
                self.send_reply(
                    message,
                    "There are no lunch plans to RSVP to! Why not add one using the make-plan command?",
                )
            else:
                try:
                    int(message_args[1])
                except ValueError:
                    self.send_reply(
                        message,
                        "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.",
                    )
                    return

                rsvp_id = int(message_args[1])
                lunch_list = self.storage.get("lunches")

                if rsvp_id >= len(lunch_list) or rsvp_id < 0:
                    self.send_reply(
                        message,
                        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
                    )
                    return

                selected_lunch = lunch_list[rsvp_id]

                if message["display_recipient"] in selected_lunch["rsvps"]:
                    self.send_reply(
                        message,
                        "You've already RSVP'd to this lunch_id! Type my-plans to show all of your current lunch plans.",
                    )
                    return

                selected_lunch["rsvps"].append(message["display_recipient"])

                lunch_list[rsvp_id] = selected_lunch
                self.storage.put("lunches", lunch_list)

                self.send_reply(
                    message,
                    "Thanks for RSVPing to lunch  at {}! Enjoy your food, {}!".format(
                        selected_lunch["restaurant"], message["display_recipient"],
                    ),
                )

        if message_args[0] == "un-rsvp" or message_args[0] == "flake":
            # less than one arguments (doesnt have message_args[1])
            if len(message_args) < 2:
                self.send_reply(
                    message,
                    "Oops! The un-rsvp command requires more information. Type help for formatting instructions.",
                )
                return

            if (
                not (self.storage.contains("lunches"))
                or len(self.storage.get("lunches")) == 0
            ):
                self.send_reply(
                    message,
                    "There are no lunch plans to remove your RSVP from! Why not add one using the make-plan command?",
                )
            else:
                try:
                    int(message_args[1])
                except ValueError:
                    self.send_reply(
                        message,
                        "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.",
                    )
                    return

                rsvp_id = int(message_args[1])
                lunch_list = self.storage.get("lunches")

                if rsvp_id >= len(lunch_list) or rsvp_id < 0:
                    self.send_reply(
                        message,
                        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
                    )
                    return

                selected_lunch = lunch_list[rsvp_id]

                if not message["display_recipient"] in selected_lunch["rsvps"]:
                    self.send_reply(
                        message,
                        "Oops! It looks like you haven't RSVP'd to this lunch_id!",
                    )
                    return

                selected_lunch["rsvps"].remove(message["display_recipient"])

                lunch_list[rsvp_id] = selected_lunch
                self.storage.put("lunches", lunch_list)

                self.send_reply(
                    message,
                    "You've successfully un-RSVP'd to lunch at "
                    + selected_lunch["restaurant"]
                    + ".",
                )

        if message_args[0] == "delete-plan":
            # less than one arguments (doesnt have message_args[1])
            if len(message_args) < 2:
                self.send_reply(
                    message,
                    "Oops! The delete-plan command requires more information. Type help for formatting instructions.",
                )
                return

            if (
                not (self.storage.contains("lunches"))
                or len(self.storage.get("lunches")) == 0
            ):
                self.send_reply(
                    message,
                    "There are no lunch plans to delete! Why not add one using the make-plan command?",
                )
            else:
                try:
                    int(message_args[1])
                except ValueError:
                    self.send_reply(
                        message,
                        "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.",
                    )
                    return

                delete_id = int(message_args[1])
                lunch_list = self.storage.get("lunches")

                if delete_id >= len(lunch_list) or delete_id < 0:
                    self.send_reply(
                        message,
                        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
                    )
                    return

                del lunch_list[delete_id]
                self.storage.put("lunches", lunch_list)

                self.send_reply(
                    message, "You've successfully deleted lunch {}.".format(delete_id)
                )  # See the updated list using the show-plans command!".format(delete_id))
                for i, lunch in enumerate(lunch_list):
                    print(
                        str(i)
                        + ": "
                        + lunch["restaurant"]
                        + " @ "
                        + lunch["time"]
                        + ", "
                        + str(len(lunch["rsvps"]))
                        + " RSVP(s)"
                    )

        # bot_handler.send_message(dict(
        #     type='stream',
        #     to='lunch',
        #     subject='yum',
        #     content='hello'
        # ))

    def is_valid_command(self, command):
        commands = [
            "help",
            "make-plan",
            "show-plans",
            "delete-plan",
            "rsvp",
            "un-rsvp",
            "flake",
            "my-plans",
        ]
        return command in commands

    def send_reply(self, original_message: Dict[str, Any], new_message: str):
        """
        Given an original message, send a string reply. Uses the metadata from
        the original message to determine to whom the response should be
        addressed.
        """
        self.client.send_message(
            {
                "type": "private",
                "to": [
                    recipient["email"]
                    for recipient in original_message["display_recipient"]
                    if self.client.email != recipient["email"]
                ],
                "content": new_message,
            }
        )

