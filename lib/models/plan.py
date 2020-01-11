from typing import List

from lib.models.user import User


class Plan:
    def __init__(self, restaurant: str, time: str, rsvps: List[User]):
        self.restaurant = restaurant
        self.time = time
        self.rsvps = rsvps
