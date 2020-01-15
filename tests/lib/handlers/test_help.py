from lib.handlers.help import HELP_MESSAGE
from lib.handlers.help import handle_help


def test_help_success(mock_client, mock_storage, mock_send_reply, make_zulip_message):
    message, args = make_zulip_message("help")
    handle_help(
        mock_client, mock_storage, message, args,
    )

    mock_send_reply.assert_called_with(
        mock_client, message, HELP_MESSAGE,
    )
