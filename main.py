import argparse
import asyncio
import time

import requests
import telegram


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="API token received from @BotFather")
    parser.add_argument("chat_id")
    args = parser.parse_args()

    token = args.token
    chat_id = args.chat_id

    while True:
        inspiration_request = requests.get("http://api.goprogram.ai/inspiration")
        if inspiration_request.status_code == 200:
            inspiration_dict = inspiration_request.json()
            msg = f"_{inspiration_dict['quote']}_\n{inspiration_dict['author']}"

            try:
                bot = telegram.Bot(token)

                async with bot:
                    await bot.send_message(text=msg, chat_id=chat_id, parse_mode="markdown")

            except telegram.error.InvalidToken:
                print(f"please check your token.\nthe value '{token}' is not valid")
                exit(-1)
            except telegram.error.BadRequest:
                print(f"please check your chat_id.\nthe value '{chat_id}' is not valid")
                exit(-1)

        # quotes are updated once an hour
        time.sleep(3600)


if __name__ == '__main__':
    asyncio.run(main())
