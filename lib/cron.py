import sched
import threading
import time
from typing import Callable
from typing import Dict
from typing import Optional
import uuid


class Cron:
    """
    Provides a cron-like interface for other classes to use. Wraps around sched
    to provide a more user-friendly interface to schedule and execute events.
    """

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.scheduled_events: Dict[uuid.UUID, sched.Event] = {}

        self.scheduler_thread = threading.Thread(daemon=True, target=self._event_loop,)
        self.scheduler_thread.start()

    def _event_loop(self):
        """
        Runs in the background in self.scheduler_thread to run Callables when
        they're scheduled.
        """
        while True:
            self.scheduler.run(blocking=True)
            time.sleep(1)

    def add_event(
        self,
        event_time: float,
        event_action: Callable,
        event_id: Optional[uuid.UUID] = None,
    ) -> uuid.UUID:
        """
        Adds an event to the queue at a given time.
        """
        if event_id is None:
            event_id = uuid.uuid4()

        self.scheduled_events[event_id] = self.scheduler.enterabs(
            event_time, 0, event_action,
        )

        return event_id

    def remove_event(self, event_id: uuid.UUID) -> bool:
        """
        Given an event's ID, removes it from the queue. Returns True iff the
        the event ID exists in the queue.
        """
        if event_id not in self.scheduled_events:
            return False

        try:
            self.scheduler.cancel(self.scheduled_events[event_id])
        except ValueError:
            return False

        self.scheduled_events.pop(event_id)

        return True
