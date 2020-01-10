import os
import sys
from typing import List
import zulip

import lunch_bot


ENV_VAR__ZULIP_USERNAME = "ZULIP_USERNAME"
ENV_VAR_ZULIP_API_KEY = "ZULIP_API_KEY"


def main(args: List[str]):
    if ENV_ZULIP_USERNAME not in os.environ or ENV_ZULIP_API_KEY not in os.environ:
        raise KeyError(
            "{} and {} must be defined in environment variables".format(
                ENV_ZULIP_USERNAME, ENV_ZULIP_API_KEY
            )
        )

    zulip_username = os.environ[ENV_VAR_ZULIP_USERNAME]
    zulip_api_key = os.environ[ENV_VAR_ZULIP_APIKEY]

    bot = lunch_bot.LunchBotHandler(
        zulip.Client(zulip_username, zulip_api_key), zulip_username, zulip_api_key,
    )
    client.call_on_each_message(bot.handle_message)


if __name__ == "__main__":
    main(sys.argv)
