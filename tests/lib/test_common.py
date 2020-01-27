from lib.common import min_edit_distance
from lib.common import send_reply


def test_send_reply(mock_client, make_zulip_message):
    """
    Tests that send_reply functions correctly.
    """
    mock_client.email = "lunch-bot-bot@zulipchat.com"

    message, _ = make_zulip_message("help")
    send_reply(
        mock_client, message, "Here is a reply!",
    )

    mock_client.send_message.assert_called_with(
        {"type": "private", "to": ["tester@email.com",], "content": "Here is a reply!",}
    )


def test_min_edit_distance_insert():
    """
    Tests that the insert cost functions correctly. Forced to insert by making
    the source string empty.
    """
    assert 1234 == min_edit_distance("", "a", insert_cost=lambda char: 1234)


def test_min_edit_distance_delete():
    """
    Tests that the delete cost functions correctly. Forced to delete by making
    the target string empty.
    """
    assert 1234 == min_edit_distance("a", "", delete_cost=lambda char: 1234)


def test_min_edit_distance_replace():
    """
    Tests that the replace cost functions correctly.
    """
    assert 1234 == min_edit_distance(
        "a",
        "b",
        insert_cost=lambda char: 5000,
        delete_cost=lambda char: 5000,
        replace_cost=lambda source_char, target_char: 1234,
    )


def test_min_edit_distance_equal():
    """
    Ensures that when two strings are the same, the min edit distance metric has
    a cost of 0.
    """
    assert 0 == min_edit_distance("same_string", "same_string")
    assert 0 == min_edit_distance("abc", "abc")


def test_min_edit_distance():
    """
    General test cases for min edit distance between two words.
    """
    assert 1 == min_edit_distance("cat", "cats")
    assert 4 == min_edit_distance("door", "gore")
