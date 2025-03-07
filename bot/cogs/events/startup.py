from bot.bot import Bot
from bot.cogs.checks.checks import is_role_sync_ctx

import discord
from discord import app_commands
from discord.ext import commands, tasks

import logging

from datetime import datetime
from asyncio import sleep

class Startup(commands.Cog):
    def __init__(self, client:Bot):
        self.client:Bot = client
        super().__init__()

#   COMMANDS
    @app_commands.command(name="sync", description="sync commands")
    @app_commands.checks.has_role("sync")
    async def sync(self, interaction: discord.Interaction):
        await self.client.tree.sync()
        await interaction.response.send_message(content="Commands syncronized",
                                                ephemeral=True,
                                                delete_after=8
                                                )

#   COMMANDS_ERROR
    @sync.error
    async def sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                "You dont have permission to use this command",
                ephemeral=True,
                delete_after=7
                )

#   PREFIX_COMMANDS
    @commands.command(name="sync_ctx")
    @commands.check(is_role_sync_ctx)
    async def sync_ctx(self, ctx:commands.Context):
        await self.client.tree.sync()
        await ctx.message.delete()
        await ctx.author.send(
            content="Syncronized commands",
            ephemeral=True,
            delete_after=7
        )

#   PREFIX_COMMANDS_ERROR
    @sync_ctx.error
    async def sync_ctx_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                "You dont have perm to use this command.",
                ephemeral=True,
                delete_after=7
                )

    
#   EVENTS
    @commands.Cog.listener()
    async def on_ready(self):
        print("started Startup")
        # await self.client.loop.run_in_executor(None, self.get_guilds)
        self.client.loop.create_task(self.routne_on_ready())
        # self.client.loop.create_task(self.get_guilds())
        # self.client.loop.create_task(self.get_status_channel())
        # self.client.loop.create_task(self.create_sync_role())

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
       await self.routne_on_join(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with self.client.guild_mutex:
            self.client.guild.remove(guild)


#   TASKS

#   FUNCTIONS
    async def get_guilds(self):
        with self.client.guild_mutex:
            for guild in self.client.guilds:
                self.client.guild.append(guild)

    async def get_status_channel(self, guild:discord.Guild):
        for channel in guild.channels:
            if channel.name == "proxmox-status-📈":
                with self.client.status_channel_mutex:
                    self.client.status_channel.append(channel)
                print(f"Has ready Status_Channel in {guild.name}")
                break

    async def create_sync_role(self, guild: discord.Guild):
        roles = await guild.fetch_roles()
        role = discord.utils.get(roles, name="sync")
        if not role:
            await guild.create_role(name="sync",
                                    color=0xE74C3C)

    async def routne_on_join(self, guild):
        with self.client.guild_mutex:
            self.client.guild.append(guild)
            await self.create_sync_role(guild)

    async def routne_on_ready(self):
        await self.get_guilds()
        with self.client.guild_mutex:
            for guild in self.client.guild:
                await self.get_status_channel(guild)
                await self.create_sync_role(guild)
        

async def setup(client:Bot):
    await client.add_cog(Startup(client))