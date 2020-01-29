from lib.handlers.my_plans import handle_my_plans
from lib.models.plan import Plan
from lib.models.user import User


def test_handle_my_plans_no_plans(
    mock_send_reply, make_handler_params,
):
    """
    Checks that, when the user has no plans, the correct error params.message is
    shown.
    """
    params = make_handler_params("my-plans")
    handle_my_plans(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "There are no active lunch plans right now! Why not add one using the make-plan command?",
    )


def test_handle_my_plans_only_in_rsvps(
    mock_send_reply, mock_user, make_handler_params, make_time,
):
    """
    Checks that the user only appears in plans they have RSVP'd to.
    """
    params = make_handler_params("my-plans")

    plan1 = Plan("tjs", make_time(11, 00), [])
    plan2 = Plan("tjs", make_time(12, 30), [mock_user])
    params.storage.get.return_value = {
        plan1.uuid: plan1,
        plan2.uuid: plan2,
    }

    handle_my_plans(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "Here are the lunches you've RSVP'd to:\ntjs @ 12:30pm, 1 RSVP",
    )


def test_handle_my_plans_success(
    mock_send_reply, mock_user, make_handler_params, make_time,
):
    """
    Checks that, when the user has a plan, the correct list is shown.
    """
    params = make_handler_params("my-plans")

    plan = Plan("tjs", make_time(12, 30), [mock_user])
    params.storage.get.return_value = {
        plan.uuid: plan,
    }

    handle_my_plans(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "Here are the lunches you've RSVP'd to:\ntjs @ 12:30pm, 1 RSVP",
    )
