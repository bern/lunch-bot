from lib.handlers.show_plans import handle_show_plans
from lib.models.plan import Plan


def test_handle_show_plans_no_plans(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that, if there are no plans, handle_show_plans reports that to the
    user.
    """
    message, args = make_zulip_message("show-plans")
    handle_show_plans(mock_client, mock_storage, message, args)

    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "There are no lunch plans to show! Why not add one using the make-plan command?",
    )


def test_handle_show_plans_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that, if there are plans, handle_show_plans shows the user all of
    the plans.
    """
    mock_storage.get.return_value = [Plan("tjs", make_time(12, 30), [])]

    message, args = make_zulip_message("show-plans")
    handle_show_plans(mock_client, mock_storage, message, args)

    mock_send_reply.assert_called_with(
        mock_client, message, "0: tjs @ 12:30pm, 0 RSVP(s)"
    )
