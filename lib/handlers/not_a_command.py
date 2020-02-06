from lib import common
from lib.handlers import HandlerParams


def handle_not_a_command(params: HandlerParams):
    common.send_reply(
        params.client,
        params.message,
        "Oops! '{}' is not a valid lunch-bot command! Type help for a list of commands I understand :-)".format(
            params.args[0],
        ),
    )
