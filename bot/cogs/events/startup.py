from bot.bot import Bot

import discord
from discord import app_commands
from discord.ext import commands


import logging


class Startup(commands.Cog):
    def __init__(self, client:Bot):
        self.client:Bot = client
        super().__init__()

#   COMMANDS

#   EVENTS
    @commands.Cog.listener()
    async def on_ready(self):
        print("started Startup")
    
    @commands.Cog.listener()
    async def on_request_error(self, response:discord.errors.HTTPException):
        if response.status == 429:  # Erro de rate limit
            remaining = response.headers.get('X-RateLimit-Remaining', None)
            reset_after = response.headers.get('X-RateLimit-Reset-After', None)

            if remaining is not None and reset_after is not None:
                remaining = int(remaining)
                reset_after = float(reset_after)

                logging.warning(f"Rate limit quase atingido! Restando {remaining} requisições.")
                logging.warning(f"Você precisa esperar {reset_after} segundos até o reset do limite.")
#   TASKS

#   FUNCTIONS

async def setup(client:Bot):
    await client.add_cog(Startup(client))