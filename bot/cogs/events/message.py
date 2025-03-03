from bot.bot import Bot

import discord
from discord import app_commands, Interaction
from discord.ext import commands, tasks

class Messages(commands.Cog):
    def __init__(self, client:Bot):
        self.client:Bot = client
        self.clear_list = []
        super().__init__()

#   COMMANDS
    @app_commands.command(name="clear", description="clear chat msg")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def clear(self, interaction: discord.Interaction, limit:int):
        channel = interaction.channel
        user = interaction.user
        try:
            async for message in channel.history(limit=limit):
                self.clear_list.append(message)
            print(f"Message sent to {channel.name}")
            await interaction.response.send_message(content="msgs added in list", ephemeral=True, delete_after=5)
        except Exception as e:
            print(f"Error add msg in clear list {channel.name}: {e}")
            await interaction.response.send_message(content=f"Error add msg in clear list {channel.name}: {e}",
                                                    ephemeral=True, delete_after=5)

#   EVENTS
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        self.start_loop()
        print("started Messages")
    
    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        pass

#   TASKS
    @tasks.loop(seconds=1, name="clear_list_loop")
    async def clear_list_loop(self):
        try:
            for msg in self.clear_list:
                msg:discord.Message
                await msg.delete()
                self.clear_list.remove(msg)
        except Exception as e:
            print(f"Error clear_list_loop message to {e}")

#   FUNCTIONS
    def start_loop(self):
        if not self.clear_list_loop.is_running():
            self.clear_list_loop.start()
        print("Started loops from Messages")


async def setup(client:Bot):
    await client.add_cog(Messages(client))
