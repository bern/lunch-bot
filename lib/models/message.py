from typing import Any
from typing import Dict
from typing import List

# For reference, this is an example of a raw Zulip message. If you need more
# fields, then you can add any included here into the Message constructor.
#
# {
#     "id": 1234,
#     "sender_id": 5678,
#     "content": contents,
#     "recipient_id": 1337,
#     "timestamp": int(time.time()),
#     "client": "website",
#     "subject": "",
#     "subject_links": [],
#     "is_me_message": False,
#     "reactions": [],
#     "submessages": [],
#     "sender_full_name": "Test Sender",
#     "sender_short_name": "tester",
#     "sender_email": "tester@email.com",
#     "sender_realm_str": "recurse",
#     "display_recipient": [
#         {
#             "email": "tester@email.com",
#             "full_name": "Test Sender",
#             "short_name": "tester",
#             "id": 5678,
#             "is_mirror_dummy": False,
#         },
#         {
#             "id": 1337,
#             "email": "lunch-bot-bot@zulipchat.com",
#             "full_name": "Lunch Bot",
#             "short_name": "lunch-bot-bot",
#             "is_mirror_dummy": False,
#         },
#     ],
#     "type": "private",
#     "avatar_url": "https://fakeurl.com/fake_picture.png",
#     "content_type": "text/x-markdown",
# }


class DisplayRecipient:
    def __init__(
        self,
        email: str = "",
        full_name: str = "",
        id: int = 0,
        is_mirror_dummy: bool = False,
        short_name: str = "",
    ):
        self.email = email
        self.full_name = full_name
        self.id = (id,)
        self.is_mirror_dummy = is_mirror_dummy
        self.short_name = short_name

    @staticmethod
    def parse_display_recipient(
        display_recipient: Dict[str, Any]
    ) -> "DisplayRecipient":
        """
        Parses an individual display recipient. Should NOT be called on the
        list of display recipients entitled 'display_recipient'.
        """
        return DisplayRecipient(
            display_recipient["email"],
            display_recipient["full_name"],
            display_recipient["id"],
            display_recipient["is_mirror_dummy"],
            display_recipient["short_name"],
        )

    @staticmethod
    def parse_display_recipients(
        display_recipients: List[Dict[str, Any]]
    ) -> List["DisplayRecipient"]:
        """
        Parses a list of display recipients. Should be used on the entire list
        of display recipients entired 'display_recipient'.
        """
        return [
            DisplayRecipient.parse_display_recipient(display_recipient)
            for display_recipient in display_recipients
        ]


class Message:
    def __init__(
        self,
        content: str = "",
        display_recipient: List[DisplayRecipient] = [],
        sender_email: str = "",
        sender_full_name: str = "",
        sender_id: int = 0,
    ):
        self.content = content
        self.display_recipient = display_recipient
        self.sender_email = sender_email
        self.sender_full_name = sender_full_name
        self.sender_id = sender_id

    @staticmethod
    def parse_zulip_message(zulip_message: Dict[str, Any]) -> "Message":
        """
        Parses out a complete Zulip message into a well structured object.
        Assumes that all normal fields are present, and does not attempt to do
        any error checking.
        """
        return Message(
            content=zulip_message["content"],
            display_recipient=DisplayRecipient.parse_display_recipients(
                zulip_message["display_recipient"],
            ),
            sender_email=zulip_message["sender_email"],
            sender_full_name=zulip_message["sender_full_name"],
            sender_id=zulip_message["sender_id"],
        )
