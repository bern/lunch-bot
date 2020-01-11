from typing import Any
from typing import Dict
from typing import List
import zulip

from lib.state_handler import StateHandler


Message = Dict[str, Any]


class BaseHandler:
    """
    The handler type for lunch_bot messages.
    """

    def handle_message(
        self,
        client: zulip.Client,
        storage: StateHandler,
        message: Message,
        args: List[str],
    ):
        raise NotImplementedError(
            "handle_message is not implemented in {}".format(self.__class__.__name__)
        )

    def send_reply(self, client: zulip.Client, message: Message, reply: str):
        """
        Given an message object, send a string reply. Uses the metadata from
        the original message to determine to whom the response should be
        addressed.
        """
        client.send_message(
            {
                "type": "private",
                "to": [
                    recipient["email"]
                    for recipient in message["display_recipient"]
                    if client.email != recipient["email"]
                ],
                "content": reply,
            }
        )
