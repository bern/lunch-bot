from typing import List
import zulip

from lib.cron import PersistentCron
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
        cron: PersistentCron,
        message: Message,
        storage: StateHandler,
    ):
        self.args = args
        self.client = client
        self.cron = cron
        self.message = message
        self.storage = storage
