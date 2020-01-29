from datetime import datetime
from typing import List
from typing import Tuple
import pytest

from lib import common
from lib.handlers import HandlerParams
from lib.models.message import DisplayRecipient
from lib.models.message import Message
from lib.models.user import User


@pytest.fixture(autouse=True)
def mock_time(mocker):
    mocker.patch(
        "lib.common.get_now",
        return_value=datetime(year=2020, month=1, day=24, hour=10, minute=0, second=0,),
    )


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
def mock_user():
    return User(email="tester@email.com", full_name="Test Sender", id=5678)


@pytest.fixture
def make_zulip_message(mock_user: User):
    def _make_zulip_message(contents: str) -> Tuple[Message, List[str]]:
        message = Message(
            content=contents,
            display_recipient=[
                DisplayRecipient(
                    email=mock_user.email,
                    full_name=mock_user.full_name,
                    is_mirror_dummy=False,
                    id=mock_user.id,
                    short_name="tester",
                ),
                DisplayRecipient(
                    email="lunch-bot-bot@zulipchat.com",
                    full_name="Lunch Bot",
                    id=1337,
                    is_mirror_dummy=False,
                    short_name="lunch-bot-bot",
                ),
            ],
            sender_email=mock_user.email,
            sender_full_name=mock_user.full_name,
            sender_id=mock_user.id,
        )
        args = contents.split()

        return message, args

    return _make_zulip_message


@pytest.fixture
def make_handler_params(mock_client, mock_storage, make_zulip_message):
    def _make_handler_params(contents: str):
        message, args = make_zulip_message(contents)

        return HandlerParams(
            args=args, client=mock_client, message=message, storage=mock_storage,
        )

    return _make_handler_params


@pytest.fixture
def make_time():
    def _make_time(hour: int, minute: int) -> datetime:
        now = common.get_now()
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
