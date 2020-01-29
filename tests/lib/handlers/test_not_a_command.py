from lib.handlers.not_a_command import handle_not_a_command


def test_handle_not_a_command_success(
    mock_send_reply, make_handler_params,
):
    """
    Ensures that the handle_not_a_command handler provides the correct response
    when an incorrect command is issued.
    """
    params = make_handler_params("blargh")
    handle_not_a_command(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "Oops! 'blargh' is not a valid lunch-bot command! Type help for a list of commands I understand :-)",
    )
