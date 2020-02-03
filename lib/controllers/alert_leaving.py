import zulip

from lib import common
from lib.models.plan import Plan


def alert_leaving(client: zulip.Client, plan: Plan):
    """
    Controller for alert_leaving. Executes if everything else goes well.
    """
    now = common.get_now()
    client.send_message(
        {
            "type": "private",
            "to": [user.email for user in plan.rsvps],
            "content": "Heads up! You're going to {} in {}".format(
                plan.restaurant, str(plan.time - now),
            ),
        }
    )
