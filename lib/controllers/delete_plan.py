import zulip

from lib.models.plan import Plan
from lib.state_handler import StateHandler


def delete_plan(client: zulip.Client, storage: StateHandler, plan: Plan):
    """
    Backend for deleting a plan from the database.
    """
    plans = storage.get(StateHandler.PLANS_ENTRY)
    if plan.uuid in plans:
        del plans[plan.uuid]
        storage.put(storage.PLANS_ENTRY, plans)
