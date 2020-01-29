from lib.handlers.show_plans import handle_show_plans
from lib.models.plan import Plan


def test_handle_show_plans_no_plans(
    mock_send_reply, make_handler_params,
):
    """
    Ensures that, if there are no plans, handle_show_plans reports that to the
    user.
    """
    params = make_handler_params("show-plans")
    handle_show_plans(params)

    mock_send_reply.assert_called_with(
        params.client,
        params.message,
        "There are no lunch plans to show! Why not add one using the make-plan command?",
    )


def test_handle_show_plans_success(
    mock_send_reply, make_handler_params, make_time,
):
    """
    Ensures that, if there are plans, handle_show_plans shows the user all of
    the plans.
    """
    params = make_handler_params("show-plans")

    plan = Plan("tjs", make_time(12, 30), [])
    params.storage.get.return_value = {
        plan.uuid: plan,
    }

    handle_show_plans(params)

    mock_send_reply.assert_called_with(
        params.client, params.message, "tjs @ 12:30pm, 0 RSVPs"
    )
