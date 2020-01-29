import pytest

from lib.handlers.delete_plan import handle_delete_plan
from lib.state_handler import StateHandler
from lib.models.plan import Plan


def test_handle_delete_plan_bad_args(
    mock_send_reply, make_handler_params,
):
    """
    Ensures that, when handle_delete_plan is provided with too few or too many
    arguments, it does not perform any action, and that it sends the correct
    response.
    """
    params = make_handler_params("delete-plan")
    handle_delete_plan(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "Oops! The delete-plan command requires more information. Type help for formatting instructions.",
    )


def test_handle_delete_plan_no_plans(
    mock_send_reply, make_handler_params,
):
    """
    Ensures that handle_delete_plan functions correctly when the StateHandler
    has no plans available to use.
    """
    params = make_handler_params("delete-plan tjs")
    handle_delete_plan(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "There are no lunch plans to delete! Why not add one using the make-plan command?",
    )


def test_handle_delete_plan_bad_id(
    mock_send_reply, make_handler_params, make_time,
):
    """
    Ensures that handle_delete_plan functions correctly when the user provides
    an integer ID that does not correspond to a plan.
    """
    params = make_handler_params("delete-plan not-tjs")

    plan = Plan("tjs", make_time(12, 30), [])
    params.storage.get.return_value = {plan.uuid: plan}

    handle_delete_plan(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
    )


def test_handle_delete_plan_ambiguous(
    mock_send_reply, make_handler_params, make_time,
):
    """
    Tests that when there are multiple plans with the same name, delete_plan
    prompts the user to disambiguate a lunch.
    """
    params = make_handler_params("delete-plan tjs")

    plan1 = Plan("tjs", make_time(11, 00), [])
    plan2 = Plan("tjs", make_time(12, 30), [])
    params.storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    handle_delete_plan(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        """There are multiple lunches with that lunch_id. Please reissue the command with the time of the lunch you're interested in:
tjs @ 11:00am
tjs @ 12:30pm""",
    )


def test_handle_delete_plan_disambiguate(
    mock_send_reply, make_handler_params, make_time,
):
    """
    Tests that when there are multiple plans with the same name, delete_plan
    lets the user disambiguate with a time.
    """
    params = make_handler_params("delete-plan tjs 12:30")

    plan1 = Plan("tjs", make_time(11, 00), [])
    plan2 = Plan("tjs", make_time(12, 30), [])
    params.storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    handle_delete_plan(params)

    params.storage.put.assert_called_with(
        params.storage.PLANS_ENTRY, {plan1.uuid: plan1}
    )
    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "You've successfully deleted lunch tjs @ 12:30pm.",
    )


def test_handle_delete_plan_success(
    mock_send_reply, make_handler_params, make_time,
):
    params = make_handler_params("delete-plan tjs")

    plan = Plan("tjs", make_time(12, 30), [])
    params.storage.get.return_value = {plan.uuid: plan}

    handle_delete_plan(params)

    params.storage.put.assert_called_with(params.storage.PLANS_ENTRY, {})
    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "You've successfully deleted lunch tjs @ 12:30pm.",
    )
