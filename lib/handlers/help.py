from lib import common
from lib.handlers import HandlerParams


HELP_MESSAGE = """
Lunch Bot Help

Available Commands:

`help` Displays all available commands that Lunch Bot understands

`make-plan [restaurant] [time]` Creates a lunch plan for a given place and time. [restaurant] and [time] must not contain any spaces.

`show-plans` Shows all active lunch plans along with their associated lunch_id

`rsvp [restaurant] (time)` RSVPs to a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command. If there are multiple lunch plans at the same restaurant, use the time to disambiguate them.

`my-plans` Shows all lunch plans you have currently RSVP'd to.

`un-rsvp [restaurant] (time)` Removes your RSVP from a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command. If there are multiple lunch plans at the same restaurant, use the time to disambiguate them.

`delete-plan [restaurant] (time)` Deletes a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command. If there are multiple lunch plans at the same restaurant, use the time to disambiguate them."""


def handle_help(params: HandlerParams):
    common.send_reply(
        params.client, params.message, HELP_MESSAGE,
    )
