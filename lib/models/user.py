from lib.models.message import Message


class User:
    def __init__(self, full_name: str, id: int):
        self.full_name = full_name
        self.id = id

    def __eq__(self, other: object) -> bool:
        """
        Determines whether two users are the same user. Naively assumes that
        two users who share the same ID must be the same user.
        """
        if not isinstance(other, User):
            return False
        return self.id == other.id

    @staticmethod
    def get_sender(message: Message) -> "User":
        """
        Given a message from Zulip, construct the user that is the sender.
        """
        return User(message.sender_full_name, message.sender_id)
