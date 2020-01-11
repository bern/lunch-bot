from typing import List
import zulip

from lib.handlers.base_handler import BaseHandler
from lib.handlers.base_handler import Message
from lib.state_handler import StateHandler


class ShowPlansHandler(BaseHandler):
    def handle_message(
        self,
        client: zulip.Client,
        storage: StateHandler,
        message: Message,
        args: List[str],
    ):
        if not storage.contains("lunches") or len(storage.get("lunches")) == 0:
            self.send_reply(
                message,
                "There are no lunch plans to show! Why not add one using the make-plan command?",
            )
            return

        self.send_reply(
            client,
            message,
            "\n".join(
                [
                    "{}: {} @ {}, {} RSVP(s)".format(
                        i, lunch["restaurant"], lunch["time"], len(lunch["rsvps"]),
                    )
                    for i, lunch in enumerate(storage.get("lunches"))
                ]
            ),
        )
