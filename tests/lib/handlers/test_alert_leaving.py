import pytest

from lib.handlers.alert_leaving import handle_alert_leaving
from lib.models.plan import Plan


@pytest.mark.parametrize(
    "args", ["alert-leaving", "alert-leaving tjs 12:30 another-arg"]
)
def test_alert_leaving_not_bad_args(mock_send_reply, make_handler_params, args):
    """
    Ensures that, when handle_alert_leaving is not provided with the correct
    number of args, it fails as expected.
    """
    params = make_handler_params(args)
    handle_alert_leaving(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "Oops! The alert-leaving command requires 1 or 2 arguments. Type help"
        " for formatting instructions.",
    )


def test_alert_leaving_no_plans(mock_send_reply, make_handler_params):
    """
    Ensures that, when there are not plans, handle_alert_leaving fails as
    expected.
    """
    params = make_handler_params("alert-leaving tjs")
    handle_alert_leaving(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "There are no existing plans. Why not create one?",
    )


def test_alert_leaving_bad_id(mock_send_reply, make_handler_params, make_time):
    """
    Ensures that, when there is a plan but not with the ID the user has
    provided, handle_alert_leaving fails as expected.
    """
    params = make_handler_params("alert-leaving not-tjs")

    plan = Plan("tjs", make_time(12, 30), [])
    params.storage.get.return_value = {
        plan.uuid: plan,
    }

    handle_alert_leaving(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and"
        " its associated lunch plan.",
    )


def test_alert_leaving_ambiguous(mock_send_reply, make_handler_params, make_time):
    """
    Ensures that, when there are multiple plans, and the user has addressed them
    ambiguously, handle_alert_leaving fails as expected.
    """
    params = make_handler_params("alert-leaving tjs")

    plan1 = Plan("tjs", make_time(11, 0), [])
    plan2 = Plan("tjs", make_time(12, 30), [])
    params.storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    handle_alert_leaving(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "There are multiple lunches with that lunch_id. Please reissue the"
        " command with the time of the lunch you're interested in:\n"
        "tjs @ 11:00am\n"
        "tjs @ 12:30pm",
    )


def test_alert_leaving_disambiguate(mock_user, make_handler_params, make_time):
    """
    Ensures that, when there are multiple plans, but the user has addressed a
    specific plan, handle_alert_leaving succeeds.
    """
    params = make_handler_params("alert-leaving tjs 12:30pm")

    plan1 = Plan("tjs", make_time(11, 0), [])
    plan2 = Plan("tjs", make_time(12, 30), [mock_user, mock_user])
    params.storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    handle_alert_leaving(params)
    params.client.send_message.assert_called_with(
        {
            "type": "private",
            "to": ["tester@email.com", "tester@email.com"],
            "content": "Heads up! You're going to tjs in 2:30:00",
        }
    )


def test_alert_leaving_success(mock_user, make_handler_params, make_time):
    """
    Ensures that, when all the preconditions have been met, handle_alert_leaving
    succeeds.
    """
    params = make_handler_params("alert-leaving tjs")

    plan = Plan("tjs", make_time(12, 30), [mock_user, mock_user, mock_user])
    params.storage.get.return_value = {
        plan.uuid: plan,
    }

    handle_alert_leaving(params)
    params.client.send_message.assert_called_with(
        {
            "type": "private",
            "to": ["tester@email.com", "tester@email.com", "tester@email.com"],
            "content": "Heads up! You're going to tjs in 2:30:00",
        }
    )
