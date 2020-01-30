import uuid

from lib.handlers.make_plan import handle_make_plan
from lib.models.plan import Plan
from lib.models.user import User


def test_handle_make_plan_bad_args(
    mock_send_reply, make_handler_params,
):
    """
    Ensures that, when we provide handle_make_plan with an improper number of
    arugments, it does not execute and provides us with the correct error
    params.message.
    """
    params = make_handler_params("make-plan tjs 12:30 and-another-arg")
    handle_make_plan(params)

    params.storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "Oops! The make-plan command requires more information. Type help for formatting instructions.",
    )


def test_handle_make_plan_existing_plan(
    mock_send_reply, make_handler_params, make_time,
):
    """
    Ensures that, when there is already an existing plan with the intended name,
    we prevent the user from making another one.
    """
    params = make_handler_params("make-plan tjs 12:30")

    plan = Plan("tjs", make_time(12, 30), [])
    params.storage.get.return_value = {plan.uuid: plan}

    handle_make_plan(params)

    params.storage.put.assert_not_called()
    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "Sorry, there is already a plan with that name and time. How about you RSVP instead?",
    )


def test_handle_make_plan_success(
    mocker, mock_send_reply, mock_user, make_handler_params, make_time,
):
    """
    Ensures that make_plan correctly inserts a plan when the arguments are
    correct.
    """
    params = make_handler_params("make-plans tjs 12:30")

    mocker.patch("uuid.uuid4", return_value="test_uuid")
    params.storage.get.return_value = {}

    handle_make_plan(params)

    params.storage.put.assert_called_with(
        params.storage.PLANS_ENTRY,
        {"test_uuid": Plan("tjs", make_time(12, 30), [mock_user])},
    )

    params.cron.add_event.assert_called()

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "I have added your plan! Enjoy lunch, Test Sender!",
    )
