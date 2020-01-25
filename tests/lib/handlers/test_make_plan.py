from lib.handlers.make_plan import handle_make_plan
from lib.models.plan import Plan
from lib.models.user import User


def test_handle_make_plan_bad_args(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that, when we provide handle_make_plan with an improper number of
    arugments, it does not execute and provides us with the correct error
    message.
    """
    message, args = make_zulip_message("make-plan tjs 12:30 and-another-arg")
    handle_make_plan(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Oops! The make-plan command requires more information. Type help for formatting instructions.",
    )


def test_handle_make_plan_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that make_plan correctly inserts a plan when the arguments are
    correct.
    """
    mock_storage.get.return_value = []

    message, args = make_zulip_message("make-plans tjs 12:30")
    handle_make_plan(mock_client, mock_storage, message, args)

    mock_storage.put.assert_called_with(
        mock_storage.PLANS_ENTRY,
        [Plan("tjs", make_time(12, 30), [User("Test Sender", 5678)])],
    )
