from datetime import datetime
import regex as re
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

    try:
        plan_time = parse_time(args[2])
    except ValueError as e:
        common.send_reply(
            client,
            message,
            "Sorry, the time you entered could not be used because it is not a valid date format.",
        )
        return

    now = common.get_now()
    if plan_time < now:
        print(plan_time, now)
        common.send_reply(
            client,
            message,
            "Sorry, you can't plan for a lunch before the current time.",
        )
        return

    user = User.get_sender(message)
    plan = Plan(args[1], plan_time, [user])

    if not storage.contains(storage.PLANS_ENTRY):
        storage.put(storage.PLANS_ENTRY, [])

    lunch_list = storage.get(storage.PLANS_ENTRY)
    lunch_list.append(plan)
    storage.put(storage.PLANS_ENTRY, lunch_list)

    common.send_reply(
        client,
        message,
        "I have added your plan! Enjoy lunch, {}!".format(user.full_name),
    )


def parse_time(date_str: str) -> datetime:
    """
    Parses out a string-formatted date into a well-structured datetime in UTC.
    Supports any of the following formats:

      - hh:mm

        In this format, we treat the value of the hh section to be 24hr format.
        If a user types in 1:00, it will be interpreted as 1am, not 1pm.

      - hh:mm(am|pm)

        In this format, we treat the value of the hh section to be 12hr format,
        and we rely on the am/pm flag to determine whether it is in the morning
        or the afternoon.
    """
    match = re.match(r"(\d?\d):(\d\d)(am|pm)?", date_str)
    if match is None:
        raise ValueError()

    groups = match.groups()
    hour = int(groups[0])
    minute = int(groups[1])
    if groups[2] == "pm" and hour < 12:
        hour += 12

    now = common.get_now()
    time = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )

    return time
