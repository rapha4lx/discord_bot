import discord
from discord import app_commands
from discord.ext import commands

from threading import Lock

import logging

class Bot(commands.Bot):
    def __init__(self, logger:logging.Logger, daemon_logger:logging.Logger):
        self.logger: logging.Logger = logger
        self.daemon_logger: logging.Logger = daemon_logger

        perm:discord.Intents = discord.Intents.default()
        perm.message_content = True
        perm.members = True

        self.rated_limit = False
        self.rated_limit_mutex = Lock()
        
        self.await_limit:float = 0
        self.await_limit_mutex = Lock()

        self.guild:list[discord.Guild] = []
        self.guild_mutex = Lock()

        self.status_channel:list[discord.TextChannel] = []
        self.status_channel_mutex = Lock()

        super().__init__(command_prefix='.', intents=perm)
    
    async def load(self):
        # for cogs in os.listdir(f'bot/cogs'):
        #     for extension in os.listdir(f'bot/cogs/{cogs}'):
        #         if extension.endswith('.py'):
        #             print(f"bot.cogs.{cogs}.{extension[:-3]}") #this [:-3] give the last 3 word of the extension
        #             await super().load_extension(f"bot.cogs.{cogs}.{extension[:-3]}")
        await super().load_extension(f"bot.cogs.events.startup")
        await super().load_extension(f"bot.cogs.events.proxmox_status")
        await super().load_extension(f"bot.cogs.events.message")

    async def on_shutdown(self):
        self.daemon_logger.warning("Daemon Shutdown")
        await self.close()
    
    async def on_restart(self):
        self.daemon_logger.info("Daemon Restart")
        await self.close()
