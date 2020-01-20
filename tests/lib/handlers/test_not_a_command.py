from lib.handlers.not_a_command import handle_not_a_command


def test_handle_not_a_command_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that the handle_not_a_command handler provides the correct response
    when an incorrect command is issued.
    """
    message, args = make_zulip_message("blargh")
    handle_not_a_command(
        mock_client, mock_storage, message, args,
    )

    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Oops! 'blargh' is not a valid lunch-bot command! Type help for a list of commands I understand :-)",
    )
