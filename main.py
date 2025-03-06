import asyncio

from bot.bot import Bot

from time import sleep
import os
from dotenv import load_dotenv

load_dotenv(".env")

client = Bot()
read = False

async def main():
    global client
    global read

    print("test")
    await client.load()
    read = True

asyncio.run(main())

while not read:
    sleep(1)

botkey = os.environ['BOT_KEY']

client.run(botkey)

