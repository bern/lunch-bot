import uuid


from lib.cron import CronEvent
from lib.cron import PersistentCron
from lib.events import AlertLeavingGenerator
from lib.models.plan import Plan
from lib.state_handler import StateHandler


def test_persistent_cron_add_event(mock_client, mock_storage, mock_user, make_time):
    mock_storage.get.return_value = {}

    cron = PersistentCron(mock_client, mock_storage)
    leaving_generator = AlertLeavingGenerator(
        Plan("tjs", make_time(12, 30), [mock_user],)
    )
    event_id = cron.add_event(1337, leaving_generator)

    cron.storage.put.assert_called_with(
        StateHandler.EVENTS_ENTRY,
        {
            event_id: CronEvent(
                event_generator=leaving_generator, event_id=event_id, event_time=1337,
            )
        },
    )


def test_persistent_cron_remove_event(mock_client, mock_storage, mock_user, make_time):
    event_id = uuid.uuid4()
    leaving_generator = AlertLeavingGenerator(
        Plan("tjs", make_time(12, 30), [mock_user])
    )
    cron_event = CronEvent(
        event_generator=leaving_generator, event_id=event_id, event_time=1337,
    )

    mock_storage.get.return_value = {
        event_id: cron_event,
    }

    cron = PersistentCron(mock_client, mock_storage)

    assert cron.remove_event(event_id)
