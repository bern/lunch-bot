def run():
    return """
Lunch Bot Help

Available Commands:

`help` Displays all available commands that Lunch Bot understands

`make-plan [restaurant] [time]` Creates a lunch plan for a given place and time. [restaurant] and [time] must not contain any spaces.

`show-plans` Shows all active lunch plans along with their associated lunch_id

`rsvp [lunch_id]` RSVPs to a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command.

`my-plans` Shows all lunch plans you have currently RSVP'd to.

`un-rsvp [lunch_id]` Removes your RSVP from a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command.

`delete-plan [lunch_id]` Deletes a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command."""
