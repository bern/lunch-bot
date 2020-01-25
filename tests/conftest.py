from datetime import datetime
import time
from typing import List
from typing import Tuple
import pytest

from lib.models.message import Message


@pytest.fixture
def mock_client(mocker):
    return mocker.patch("zulip.Client")


@pytest.fixture
def mock_storage(mocker):
    return mocker.patch("lib.state_handler.StateHandler")


@pytest.fixture
def mock_send_reply(mocker):
    return mocker.patch("lib.common.send_reply")


@pytest.fixture
def make_zulip_message():
    def _make_zulip_message(contents: str) -> Tuple[Message, List[str]]:
        message = {
            "id": 1234,
            "sender_id": 5678,
            "content": contents,
            "recipient_id": 1337,
            "timestamp": int(time.time()),
            "client": "website",
            "subject": "",
            "subject_links": [],
            "is_me_message": False,
            "reactions": [],
            "submessages": [],
            "sender_full_name": "Test Sender",
            "sender_short_name": "tester",
            "sender_email": "tester@email.com",
            "sender_realm_str": "recurse",
            "display_recipient": [
                {
                    "email": "tester@email.com",
                    "full_name": "Test Sender",
                    "short_name": "tester",
                    "id": 5678,
                    "is_mirror_dummy": False,
                },
                {
                    "id": 1337,
                    "email": "lunch-bot-bot@zulipchat.com",
                    "full_name": "Lunch Bot",
                    "short_name": "lunch-bot-bot",
                    "is_mirror_dummy": False,
                },
            ],
            "type": "private",
            "avatar_url": "https://fakeurl.com/fake_picture.png",
            "content_type": "text/x-markdown",
        }
        args = contents.split()

        return message, args

    return _make_zulip_message


@pytest.fixture
def make_time():
    def _make_time(hour: int, minute: int) -> datetime:
        now = datetime.now()
        return datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
        )

    return _make_time
