from lib.handlers.un_rsvp import handle_un_rsvp
from lib.models.plan import Plan
from lib.models.user import User


def test_handle_un_rsvp_bad_args(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that handle_un_rsvp fails as expected when we don't provide the
    correct number of arguments.
    """
    message, args = make_zulip_message("un-rsvp tjs adfg as")
    handle_un_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Oops! The un-rsvp command requires more information. Type help for formatting instructions.",
    )


def test_handle_un_rsvp_no_lunches(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that handle_un_rsvp fails as expected when there are not lunches to
    un-rsvp from.
    """
    message, args = make_zulip_message("un-rsvp tjs")
    handle_un_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "There are no lunch plans to remove your RSVP from! Why not add one using the make-plan command?",
    )


def test_handle_un_rsvp_bad_id(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that handle_un_rsvp fails as expected when the user provides an id
    that is out of range of our available lunches.
    """
    plan = Plan("tjs", make_time(12, 30), [User("Test Sender", 5678)])
    mock_storage.get.return_value = {
        plan.uuid: plan,
    }

    message, args = make_zulip_message("un-rsvp not-tjs")
    handle_un_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
    )


def test_handle_un_rsvp_not_rsvpd(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that handle_un_rsvp fails as expected when the user is not already
    RSVP'd to the event.
    """
    plan = Plan("tjs", make_time(12, 30), [])
    mock_storage.get.return_value = {
        plan.uuid: plan,
    }

    message, args = make_zulip_message("un-rsvp tjs")
    handle_un_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client, message, "Oops! It looks like you haven't RSVP'd to this lunch_id!"
    )


def test_handle_un_rsvp_ambiguous(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that, when the user has provided an ambiguous query, handle_un_rsvp
    prompts them to disambiguate.
    """
    plan1 = Plan("tjs", make_time(11, 00), [])
    plan2 = Plan("tjs", make_time(12, 30), [])
    mock_storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    message, args = make_zulip_message("un-rsvp tjs")
    handle_un_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        mock_client,
        message,
        """There are multiple lunches with that lunch_id. Please reissue the command with the time of the lunch you're interested in:
tjs @ 11:00am
tjs @ 12:30pm""",
    )


def test_handle_un_rsvp_disambiguate(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that, when the user has provided an ambiguous query, handle_un_rsvp
    prompts them to disambiguate.
    """
    plan1 = Plan("tjs", make_time(11, 00), [])
    plan2 = Plan("tjs", make_time(12, 30), [User("Test Sender", 5678)])
    mock_storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    message, args = make_zulip_message("un-rsvp tjs 12:30")
    handle_un_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put.assert_called_with(
        mock_storage.PLANS_ENTRY,
        {plan1.uuid: plan1, plan2.uuid: Plan("tjs", make_time(12, 30), []),},
    )
    mock_send_reply.assert_called_with(
        mock_client, message, "You've successful un-RSVP'd to lunch at tjs."
    )


def test_handle_un_rsvp_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Ensures that handle_un_rsvp succeeds when the required preconditions are
    met.
    """
    plan = Plan("tjs", make_time(12, 30), [User("Test Sender", 5678)])
    mock_storage.get.return_value = {
        plan.uuid: plan,
    }

    message, args = make_zulip_message("un-rsvp tjs")
    handle_un_rsvp(mock_client, mock_storage, message, args)

    mock_storage.put_assert_called_with(
        mock_storage.PLANS_ENTRY, Plan("tjs", make_time(12, 30), [])
    )
    mock_send_reply.assert_called_with(
        mock_client, message, "You've successful un-RSVP'd to lunch at tjs."
    )
