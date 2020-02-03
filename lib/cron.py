import sched
import threading
import time
from typing import Callable
from typing import Dict
from typing import Optional
import uuid
import zulip

from lib.events import EventGenerator
from lib.state_handler import StateHandler


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


class CronEvent:
    """
    Serializable representation of an event that may be scheduled.
    """

    def __init__(
        self,
        *,
        event_generator: EventGenerator,
        event_id: uuid.UUID,
        event_time: float,
    ):
        self.event_generator = event_generator
        self.event_id = event_id
        self.event_time = event_time


class PersistentCron:
    """
    A persistent form of Cron that automatically saves queued events to disk.
    Reloads them when starting up, so that events can be rescheduled after a
    restart.
    """

    def __init__(self, client: zulip.Client, storage: StateHandler):
        self.cron = Cron()
        self.client = client
        self.storage = storage

        events = self._get_persistent_events()
        now = time.time()
        for event in events.values():
            if event.event_time < now:
                # TODO: Decide what to do with old events
                continue

            self.cron.add_event(
                event.event_time,
                event.event_generator.generate_action(self.client, self.storage),
                event.event_id,
            )

    def _get_persistent_events(self) -> Dict[uuid.UUID, CronEvent]:
        """
        Gets the persisted copy of events from the database. If it doesn't
        exist, create it.
        """
        if not self.storage.contains(StateHandler.EVENTS_ENTRY):
            self.storage.put(StateHandler.EVENTS_ENTRY, {})
        return self.storage.get(StateHandler.EVENTS_ENTRY)

    def add_event(
        self,
        event_time: float,
        event_generator: EventGenerator,
        event_id: Optional[uuid.UUID] = None,
    ) -> uuid.UUID:
        """
        Adds an event to the queue, and persists it to disk so that it can be
        reloaded later.
        """
        event_id = self.cron.add_event(
            event_time,
            event_generator.generate_action(self.client, self.storage),
            event_id,
        )

        events = self._get_persistent_events()
        events[event_id] = CronEvent(
            event_generator=event_generator, event_id=event_id, event_time=event_time,
        )
        self.storage.put(StateHandler.EVENTS_ENTRY, events)

        return event_id

    def remove_event(self, event_id: uuid.UUID) -> bool:
        """
        Removes an event from the queue, and
        """
        events = self._get_persistent_events()

        persistent_removed = False
        if event_id in events:
            persistent_removed = True
            events.pop(event_id)

        queue_removed = self.cron.remove_event(event_id)

        return persistent_removed or queue_removed
