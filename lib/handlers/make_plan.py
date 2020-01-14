from typing import List
import zulip

from lib import common
from lib.models.message import Message
from lib.models.plan import Plan
from lib.models.user import User
from lib.state_handler import StateHandler


def handle_make_plan(
    client: zulip.Client, storage: StateHandler, message: Message, args: List[str],
):
    if len(args) != 3:
        common.send_reply(
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

    common.send_reply(
        client,
        message,
        "I have added your plan! Enjoy lunch, {}!".format(user.full_name),
    )
