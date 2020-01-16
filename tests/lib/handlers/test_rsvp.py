from lib.handlers.rsvp import handle_rsvp
from lib.models.plan import Plan
from lib.models.user import User


def test_handle_rsvp_bad_args(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that the RSVP handler will fail as expected when we provide an
    incorrect number of arguments.
    """
    message, args = make_zulip_message("rsvp tjs also-this-extra-arg")
    handle_rsvp(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Oops! The rsvp command requires more information. Type help for formatting instructions.",
    )


def test_handle_rsvp_no_plans(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that handle_rsvp fails as expected when there are no plans.
    """
    message, args = make_zulip_message("rsvp 0")
    handle_rsvp(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "There are no lunch plans to RSVP to! Why not add one using the make-plan command?",
    )


def test_handle_rsvp_malformed_id(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that handle_rsvp failes correctly when the plan ID is malformed
    (i.e. it cannot be coerced to int).
    """
    mock_storage.get.return_value = [Plan("tjs", "12:30", [])]

    message, args = make_zulip_message("rsvp not-an-id")
    handle_rsvp(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.",
    )


def test_handle_rsvp_bad_id(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that handle_rsvp failes correctly when the plan ID is not malformed
    but does not correspond to a plan.
    """
    mock_storage.get.return_value = [Plan("tjs", "12:30", [])]

    message, args = make_zulip_message("rsvp 1")
    handle_rsvp(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
    )


def test_handle_rsvp_already_rsvpd(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures handle_rsvp fails correctly when the user is already RSVP'd to the
    event to which they're trying to rsvp.
    """
    mock_storage.get.return_value = [Plan("tjs", "12:30", [User("Test Sender", 5678)])]

    message, args = make_zulip_message("rsvp 0")
    handle_rsvp(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "You've already RSVP'd to this lunch_id! Type my-plans to show all of your current lunch plans.",
    )


def test_handle_rsvp_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that handle_rsvp functions correctly when the preconditions are
    met.
    """
    mock_storage.get.return_value = [Plan("tjs", "12:30", [])]

    message, args = make_zulip_message("rsvp 0")
    handle_rsvp(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_called_with(
        mock_storage.PLANS_ENTRY, [Plan("tjs", "12:30", [User("Test Sender", 5678)])]
    )
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Thanks for RSVPing to lunch  at tjs! Enjoy your food, Test Sender!",
    )
