from lib.handlers.reset import handle_reset


def test_handle_reset_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that, when asked to reset, Lunch Bot will only do so when
    confirmed.
    """
    message, args = make_zulip_message("reset")
    handle_reset(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "This will wipe all current lunches from my records. If you wish to continue, please type 'reset confirm'.",
    )


def test_handle_rest_confirm_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that, when asked to reset, Lunch Bot will only do so when
    confirmed.
    """
    message, args = make_zulip_message("reset confirm")
    handle_reset(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_called_with(mock_storage.PLANS_ENTRY, [])
    mock_send_reply.assert_not_called()
