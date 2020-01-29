from lib.handlers.reset import handle_reset


def test_handle_reset_success(
    mock_send_reply, make_handler_params,
):
    """
    Ensures that, when asked to reset, Lunch Bot will only do so when
    confirmed.
    """
    params = make_handler_params("reset")
    handle_reset(params)

    params.storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "This will wipe all current lunches from my records. If you wish to continue, please type 'reset confirm'.",
    )


def test_handle_rest_confirm_success(
    mock_send_reply, make_handler_params,
):
    """
    Ensures that, when asked to reset, Lunch Bot will only do so when
    confirmed.
    """
    params = make_handler_params("reset confirm")
    handle_reset(params)

    params.storage.put.assert_called_with(params.storage.PLANS_ENTRY, {})
    mock_send_reply.assert_not_called()
