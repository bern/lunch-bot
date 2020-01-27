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
    message, args = make_zulip_message("rsvp tjs 12:30 fasdf")
    handle_rsvp(mock_client, mock_storage, message, args)

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
    message, args = make_zulip_message("rsvp tjs")
    handle_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "There are no lunch plans to RSVP to! Why not add one using the make-plan command?",
    )


def test_handle_rsvp_bad_id(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that handle_rsvp failes correctly when the plan ID is not malformed
    but does not correspond to a plan.
    """
    plan = Plan("tjs", make_time(12, 30), [])
    mock_storage.get.return_value = {plan.uuid: plan}

    message, args = make_zulip_message("rsvp not-tjs")
    handle_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
    )


def test_handle_rsvp_already_rsvpd(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures handle_rsvp fails correctly when the user is already RSVP'd to the
    event to which they're trying to rsvp.
    """
    plan = Plan("tjs", make_time(12, 30), [User("Test Sender", 5678)])
    mock_storage.get.return_value = {plan.uuid: plan}

    message, args = make_zulip_message("rsvp tjs")
    handle_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "You've already RSVP'd to this lunch_id! Type my-plans to show all of your current lunch plans.",
    )


def test_handle_rsvp_ambiguous(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that, when the query is ambiguous, handle_rsvp alerts the user and
    asks them to disambiguate with a time.
    """
    plan1 = Plan("tjs", make_time(11, 00), [])
    plan2 = Plan("tjs", make_time(12, 30), [])
    mock_storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    message, args = make_zulip_message("rsvp tjs")
    handle_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        """There are multiple lunches with that lunch_id. Please reissue the command with the time of the lunch you're interested in:
tjs @ 11:00am
tjs @ 12:30pm""",
    )


def test_handle_rsvp_disambiguate(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that, when there are multiple lunches, the user can construct a
    query to disambiguate between them.
    """
    plan1 = Plan("tjs", make_time(11, 00), [])
    plan2 = Plan("tjs", make_time(12, 30), [])
    mock_storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    message, args = make_zulip_message("rsvp tjs 12:30")
    handle_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_called_with(
        mock_storage.PLANS_ENTRY,
        {
            plan1.uuid: plan1,
            plan2.uuid: Plan("tjs", make_time(12, 30), [User("Test Sender", 5678)]),
        },
    )
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Thanks for RSVPing to lunch  at tjs! Enjoy your food, Test Sender!",
    )


def test_handle_rsvp_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that handle_rsvp functions correctly when the preconditions are
    met.
    """
    plan = Plan("tjs", make_time(12, 30), [])
    mock_storage.get.return_value = {
        plan.uuid: plan,
    }

    message, args = make_zulip_message("rsvp tjs")
    handle_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_called_with(
        mock_storage.PLANS_ENTRY,
        {plan.uuid: Plan("tjs", make_time(12, 30), [User("Test Sender", 5678)])},
    )
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Thanks for RSVPing to lunch  at tjs! Enjoy your food, Test Sender!",
    )
