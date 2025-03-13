from bot.bot import Bot
from bot.cogs.checks.checks import is_create_proxmox_status

import discord
from discord import app_commands
from discord.ext import commands, tasks

from asyncio import Lock

from datetime import datetime

import json

class ProxmoxStatus(commands.Cog):
    def __init__(self, client:Bot):
        self.client:Bot = client
        super().__init__()

#   COMMANDS
    @app_commands.command(name="proxmox_status", description="Add this discord to receive proxmox status")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.check(is_create_proxmox_status)
    async def proxmox_status(self, interaction: discord.Interaction):
        guild: discord.Guild = interaction.guild
        channel: discord.TextChannel = None

        channel = await guild.create_text_channel("proxmox-status-📈")
        with self.client.status_channel_mutex:
            self.client.status_channel.append(channel)

        await interaction.response.send_message(
            content="This guild added in proxmox status update",
            ephemeral=True,
            delete_after=7
            )
        await self.send_status_msg(channel)

#   COMMANDS_ERROR
    @proxmox_status.error
    async def proxmox_status_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            if not interaction.permissions.administrator:
                await interaction.response.send_message(
                    content="You dont have administrator perm",
                    ephemeral=True,
                    delete_after=7
                )
                return 
            if not is_create_proxmox_status(interaction):
                await interaction.response.send_message(
                    content="Proxmox TextChannel has exist",
                    ephemeral=True,
                    delete_after=7
                )
                return


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

        with open('/mnt/storage/containers.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
        
        for container in dados['containers']:
            embed.add_field(name='ID/Name', value=f"{container['id']} / {container['name']}")
            embed.add_field(name='Status', value=container['status'], inline=True)
            ips:str = None
            for containerIP in container['ip']:
                if ips:
                    ips += f'\n{containerIP}'
                else:
                    ips = containerIP
            embed.add_field(name='IP', value=ips, inline=True)
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