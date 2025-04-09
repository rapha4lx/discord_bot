import asyncio

from bot.bot import Bot

from time import sleep
import os
from dotenv import load_dotenv

from logs.logs import setup_logger
from daemon.daemon import setup_daemon, check_for_changes


load_dotenv(".env")
check_for_changes(os.getenv('REMOTE_CHECK_NAME'))

app_logger = setup_logger('app.log')
daemon_logger = setup_logger('daemon.log')

client = Bot(logger=app_logger, daemon_logger=daemon_logger)

ready = False

async def main():
    global client
    global ready

    await client.load()
    ready = True

asyncio.run(main())

setup_daemon(client=client)

botkey = os.environ['BOT_KEY']

while not ready:
    sleep(1)

daemon_logger.info("running")

client.run(botkey)

