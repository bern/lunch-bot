from lib.handlers.my_plans import handle_my_plans
from lib.models.plan import Plan
from lib.models.user import User


def test_handle_my_plans_no_plans(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Checks that, when the user has no plans, the correct error message is
    shown.
    """
    message, args = make_zulip_message("my-plans")
    handle_my_plans(mock_client, mock_storage, message, args)

    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "There are no active lunch plans right now! Why not add one using the make-plan command?",
    )


def test_handle_my_plans_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message, make_time
):
    """
    Checks that, when the user has a plan, the correct list is shown.
    """
    plan = Plan("tjs", make_time(12, 30), [User("Test Sender", 5678)])
    mock_storage.get.return_value = {
        plan.uuid: plan,
    }

    message, args = make_zulip_message("my-plans")
    handle_my_plans(mock_client, mock_storage, message, args)

    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Here are the lunches you've RSVP'd to:\ntjs @ 12:30pm, 1 RSVP",
    )
