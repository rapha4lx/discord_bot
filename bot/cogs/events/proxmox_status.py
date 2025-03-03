from bot.bot import Bot

import discord
from discord import app_commands
from discord.ext import commands, tasks

import asyncio


class ProxmoxStatus(commands.Cog):
    def __init__(self, client:Bot):
        self.client:Bot = client
        self.guild:list[discord.Guild] = []
        self.status_channel:list[discord.TextChannel] = []
        super().__init__()

#   COMMANDS

#   EVENTS
    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_created_status_channel()
        self.start_loops()
        print("started ProxmoxStatus")
    
#   TASKS
    @tasks.loop(minutes=5, name="update_infos")
    async def update_infos(self):
        for channel in self.status_channel:
            try:
                last_msg:discord.Message = None
                async for message in channel.history(limit=1):
                    last_msg = message

                if (last_msg is None):
                    await channel.send("test")
                    print(f"Message sent to {channel.name}")
                else:
                    embed = self.get_embed(last_msg=last_msg)
                    await last_msg.edit(content="", embed=embed)
                    print(f"Message edited to {channel.name}")
                    
            except Exception as e:
                print(f"Error sending message to {channel.name}: {e}")

        
#   FUNCTIONS
    def start_loops(self):
        if not self.update_infos.is_running():
            self.update_infos.start()
        print("Started loops from ProxmoxStatus")

    async def check_created_status_channel(self):
        channel_created = False
        guilds =  self.client.guilds
        for guild in guilds:
            self.guild.append(guild)
            for channel in guild.channels:
                if channel.name == "proxmox-status-📈":
                    channel_created = True
                    self.status_channel.append(channel)
                    print(f"Has ready Status_Channel in {guild.name}")
                    break
                channel_created = False
            if not channel_created :
                self.status_channel.append(await guild.create_text_channel("proxmox-status-📈"))
                print(f"Created Status_Channel in {guild.name}")

    def get_embed(self, last_msg:discord.Message) -> discord.Embed:
        embed = discord.Embed(
            title="Machine States",
            color=discord.Color.orange(),
            timestamp=last_msg.created_at
        )
        return (embed)


async def setup(client:Bot):
    await client.add_cog(ProxmoxStatus(client))