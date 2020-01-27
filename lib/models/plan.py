from datetime import datetime
from typing import List
import uuid

from lib.models.user import User


class Plan:
    def __init__(self, restaurant: str, time: datetime, rsvps: List[User]):
        self.uuid = uuid.uuid4()
        self.restaurant = restaurant
        self.time = time
        self.rsvps = rsvps

    def __eq__(self, other: object):
        if not isinstance(other, Plan):
            return False
        return (
            self.restaurant == other.restaurant
            and self.time == other.time
            and self.rsvps == other.rsvps
        )
