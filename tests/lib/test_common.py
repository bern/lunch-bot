from lib.common import send_reply


def test_send_reply(mock_client, make_zulip_message):
    """
    Tests that send_reply functions correctly.
    """
    mock_client.email = "lunch-bot-bot@zulipchat.com"

    message, _ = make_zulip_message("help")
    send_reply(
        mock_client, message, "Here is a reply!",
    )

    mock_client.send_message.assert_called_with(
        {"type": "private", "to": ["tester@email.com",], "content": "Here is a reply!",}
    )
