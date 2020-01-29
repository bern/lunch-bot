from typing import List
import zulip

from lib.models.message import Message
from lib.state_handler import StateHandler


class HandlerParams:
    """
    A struct that represents the arguments a handler can receive. Used to extend
    the possible arguments without having to rewrite each of the function
    definitions each time.
    """

    def __init__(
        self,
        *,
        args: List[str],
        client: zulip.Client,
        message: Message,
        storage: StateHandler,
    ):
        self.client = client
        self.storage = storage
        self.message = message
        self.args = args
