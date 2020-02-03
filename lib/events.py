from typing import Callable
import zulip

from lib.controllers.alert_leaving import alert_leaving
from lib.models.plan import Plan
from lib.state_handler import StateHandler


class EventGenerator:
    """
    Interface of a serializable object that generates the actions we store in
    PersistentCron. Used to that we can pickle these objects.
    """

    def __init__(self):
        pass

    def generate_action(self, client: zulip.Client, storage: StateHandler) -> Callable:
        raise NotImplementedError()


class AlertLeavingGenerator(EventGenerator):
    """
    Generates a call to lib.controllers.alert_leaving.
    """

    def __init__(self, plan: Plan):
        self.plan = plan

    def generate_action(self, client: zulip.Client, storage: StateHandler) -> Callable:
        return lambda: alert_leaving(client, self.plan)
