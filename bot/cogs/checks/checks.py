

import discord
from discord.ext import commands

def is_role_sync_ctx(ctx:commands.Context) -> bool:
    user:discord.Member = ctx.message.author
    roles = user.roles
    if not roles:
        return False
    role = discord.utils.get(
        user.roles,
        name="sync"
        )
    if role:
        return True
    return False

def is_create_proxmox_status(interaction: discord.Interaction) -> bool:
    channel = discord.utils.get(
            interaction.guild.text_channels,
            name="proxmox-status-📈"
        )
    if channel:
        interaction.response.send_message(
            content="Channel exist",
            ephemeral=True,
            delete_after=7
            )
        return False
    return True
