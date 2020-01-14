import zulip

from lib.models.message import Message


def send_reply(client: zulip.Client, message: Message, reply: str):
    """
    Given an message object, send a string reply. Uses the metadata from
    the original message to determine to whom the response should be
    addressed.
    """
    client.send_message(
        {
            "type": "private",
            "to": [
                recipient["email"]
                for recipient in message["display_recipient"]
                if client.email != recipient["email"]
            ],
            "content": reply,
        }
    )
