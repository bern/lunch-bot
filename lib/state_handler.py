import shelve
import traceback
from typing import Any
from typing import Optional


class StateHandler:
    """
    Custom shim that implements Zulip's StateHandler class, but with some
    changes to better suit our use case!
    """

    SHELVE_DB_FILE = "lunch-bot.db"

    OPEN_ERROR = ValueError("StateHandler must not be open")
    NOT_OPEN_ERROR = ValueError("StateHandler must be open")

    def __init__(self):
        self._db = None

    def __enter__(self):
        return self.open()
        pass

    def __exit__(self, type, value, traceback):
        self.close()

    def open(self) -> "StateHandler":
        if self.is_open():
            raise self.OPEN_ERROR

        self._db = shelve.open(self.SHELVE_DB_FILE, writeback=True)
        return self

    def is_open(self) -> bool:
        return not self._db is None

    def close(self):
        if not self.is_open():
            raise self.NOT_OPEN_ERROR

        self._db.close()

    def put(self, key: str, value: Any):
        if not self.is_open():
            raise self.NOT_OPEN_ERROR

        self._db[key] = value

    def get(self, key: str) -> Any:
        if not self.is_open():
            raise self.NOT_OPEN_ERROR

        return self._db[key]

    def contains(self, key: str) -> bool:
        if not self.is_open():
            raise self.NOT_OPEN_ERROR

        return key in self._db
