import pytest

from lib.handlers.delete_plan import handle_delete_plan
from lib.state_handler import StateHandler
from lib.models.plan import Plan


def test_handle_delete_plan_bad_args(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that, when handle_delete_plan is provided with too few or too many
    arguments, it does not perform any action, and that it sends the correct
    response.
    """
    message, args = make_zulip_message("delete-plan")
    handle_delete_plan(
        mock_client, mock_storage, message, args,
    )

    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "Oops! The delete-plan command requires more information. Type help for formatting instructions.",
    )


def test_handle_delete_plan_no_plans(
    mock_client, mock_storage, mock_send_reply, make_zulip_message,
):
    """
    Ensures that handle_delete_plan functions correctly when the StateHandler
    has no plans available to use.
    """
    message, args = make_zulip_message("delete-plan 0")
    handle_delete_plan(
        mock_client, mock_storage, message, args,
    )

    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "There are no lunch plans to delete! Why not add one using the make-plan command?",
    )


def test_handle_delete_plan_malformed_id(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that handle_delete_plan functions correctly when the user provides
    a non-integer ID.
    """
    mock_storage.get.return_value = [
        Plan("tjs", "12:30", []),
    ]

    message, args = make_zulip_message("delete-plan not-a-lunch")
    handle_delete_plan(
        mock_client, mock_storage, message, args,
    )

    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "A lunch_id must be a number! Type show-plans to see each lunch_id and its associated lunch plan.",
    )


def test_handle_delete_plan_bad_id(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    """
    Ensures that handle_delete_plan functions correctly when the user provides
    an integer ID that does not correspond to a plan.
    """
    mock_storage.get.return_value = [
        Plan("tjs", "12:30", []),
    ]

    message, args = make_zulip_message("delete-plan 1")
    handle_delete_plan(
        mock_client, mock_storage, message, args,
    )

    mock_send_reply.assert_called_with(
        mock_client,
        message,
        "That lunch_id doesn't exist! Type show-plans to see each lunch_id and its associated lunch plan.",
    )


def test_handle_delete_plan_success(
    mock_client, mock_storage, mock_send_reply, make_zulip_message
):
    mock_storage.get.return_value = [
        Plan("tjs", "12:30", []),
    ]

    message, args = make_zulip_message("delete-plan 0")
    handle_delete_plan(
        mock_client, mock_storage, message, args,
    )

    mock_storage.put.assert_called_with(mock_storage.PLANS_ENTRY, [])
    mock_send_reply.assert_called_with(
        mock_client, message, "You've successfully deleted lunch 0."
    )
