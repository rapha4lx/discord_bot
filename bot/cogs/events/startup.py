from bot.bot import Bot

import discord
from discord import app_commands
from discord.ext import commands, tasks

import logging

from datetime import datetime


class Startup(commands.Cog):
    def __init__(self, client:Bot):
        self.client:Bot = client
        super().__init__()

#   COMMANDS
    @app_commands.command(name="sync", description="sync commands")
    @app_commands.checks.has_role("sync")
    async def sync(self, interaction: discord.Interaction):
        await self.client.tree.sync()
        await interaction.response.send_message(content="Commands syncronized"
                                                , ephemeral=True, delete_after=8)

#   PREFIX_COMMANDS
    @commands.command(name="sync")
    # @commands.has_permissions(administrator=True)
    @commands.has_role("sync")
    async def sync(self, ctx:commands.Context):
        await self.client.tree.sync()
        await ctx.message.delete()
        
#   EVENTS
    @commands.Cog.listener()
    async def on_ready(self):
        print("started Startup")
        # await gather(self.get_guilds(),
        #              self.get_status_channel(),
        #              self.create_sync_role()
        #             )
        await self.client.loop.run_in_executor(None, self.get_guilds)
        self.client.loop.create_task(self.get_status_channel())
        self.client.loop.create_task(self.create_sync_role())
        
    
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
    def get_guilds(self):
        with self.client.guild_mutex:
            for guild in self.client.guild:
                self.client.guild.append(guild)

    async def get_status_channel(self):
        channel_created = False
        with self.client.guild_mutex:
            for guild in self.client.guilds:
                for channel in guild.channels:
                    if channel.name == "proxmox-status-📈":
                        channel_created = True
                        with self.client.status_channel_mutex:
                            self.client.status_channel.append(channel)
                        print(f"Has ready Status_Channel in {guild.name}")
                        break
                    channel_created = False
                if not channel_created :
                    with self.client.status_channel_mutex:
                        self.client.status_channel.append(await guild.create_text_channel("proxmox-status-📈"))
                    print(f"Created Status_Channel in {guild.name}")

    async def create_sync_role(self):
        # with self.client.guild_mutex:
        for guild in self.client.guild:
            role = discord.utils.get(guild.fetch_roles(), name="sync")
            if not role:
                await guild.create_role(name="sync",
                                        color=discord.colour.Color.red)

async def setup(client:Bot):
    await client.add_cog(Startup(client))