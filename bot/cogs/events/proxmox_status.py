from bot.bot import Bot
from bot.cogs.checks.checks import is_create_proxmox_status

import discord
from discord import app_commands
from discord.ext import commands, tasks

from asyncio import Lock

from datetime import datetime




class ProxmoxStatus(commands.Cog):
    def __init__(self, client:Bot):
        self.client:Bot = client
        super().__init__()

#   COMMANDS
    @app_commands.command(name="proxmox_status", description="Add this discord to receive proxmox status")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.check(is_create_proxmox_status)
    async def proxmox_status(self, interaction: discord.Interaction):
        user: discord.Member = interaction.user
        guild: discord.Guild = interaction.guild
        channel: discord.TextChannel = None

        with self.client.status_channel_mutex:
            channel = await guild.create_text_channel("proxmox-status-📈")
            self.client.status_channel.append(channel)

        await interaction.response.send_message(
            content="This guild added in proxmox status update",
            ephemeral=True,
            delete_after=7
            )
        await self.send_status_msg(channel)

#   EVENTS
    @commands.Cog.listener()
    async def on_ready(self):
        self.start_loops()
        print("started ProxmoxStatus")
    
#   TASKS
    @tasks.loop(minutes=4, name="update_infos")
    async def update_infos(self):
        if not self.client.status_channel:
            return 
        with self.client.status_channel_mutex:
            for channel in self.client.status_channel:
                try:
                    await self.send_status_msg(channel)
                except Exception as e:
                    print(f"Error sending message to {channel.name}: {e}")


#   FUNCTIONS
    def start_loops(self):
        if not self.update_infos.is_running():
            self.update_infos.start()
        print("Started loops from ProxmoxStatus")

    def get_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="Machine States",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        return (embed)

    async def send_status_msg(self, channel:discord.TextChannel):
        last_msg:discord.Message = None
        async for message in channel.history(limit=1):
            last_msg = message

        if (last_msg is None):
            await channel.send("test")
            print(f"Message sent to {channel.name}")
        else:
            embed = self.get_embed()
            await last_msg.edit(content="", embed=embed)
            print(f"Message edited to {channel.name}")

async def setup(client:Bot):
    await client.add_cog(ProxmoxStatus(client))