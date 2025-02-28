import asyncio

import discord

from bot.bot import Bot

from time import sleep
import os

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

