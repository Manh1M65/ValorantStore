from __future__ import annotations

import discord
from discord import app_commands, Interaction, ui
from discord.ext import commands

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from bot import ValorantBot

class Admin(commands.Cog):
    """Error handler"""

    def __init__(self, bot: ValorantBot) -> None:
        self.bot: ValorantBot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, sync_type: Literal['guild', 'global']) -> None:
        """ Sync the application commands """

        async with ctx.typing():
            if sync_type == 'guild':
                guild = discord.Object(id=ctx.guild.id)
                self.bot.tree.copy_global_to(guild=guild)
                await self.bot.tree.sync(guild=guild)
                await ctx.reply(f"Synced guild !")
                return

            await self.bot.tree.sync()
            await ctx.reply(f"Synced global !")

    @commands.command()
    @commands.is_owner()
    async def unsync(self, ctx: commands.Context, unsync_type: Literal['guild', 'global']) -> None:
        """ Unsync the application commands """

        async with ctx.typing():
            if unsync_type == 'guild':
                guild = discord.Object(id=ctx.guild.id)
                commands = self.bot.tree.get_commands(guild=guild)
                for command in commands:
                    self.bot.tree.remove_command(command, guild=guild)
                await self.bot.tree.sync(guild=guild)
                await ctx.reply(f"Un-Synced guild !")    
                return
    
            commands = self.bot.tree.get_commands()
            for command in commands:
                self.bot.tree.remove_command(command)
            await self.bot.tree.sync()
            await ctx.reply(f"Un-Synced global !")

    @app_commands.command(description='Shows basic information about the bot.')
    async def about(self, interaction: Interaction) -> None:
        """ Shows basic information about the bot. """
        
        owner_id = 920475941946396673
        owner_url = f'https://discord.com/users/{owner_id}'
        github_project = 'https://github.com/Manh1M65/ValorantStore'
        
        embed = discord.Embed(color=0xffffff)
        embed.set_author(name='ᴠᴀʟᴏʀᴀɴᴛ ʙᴏᴛ ᴘʀᴏᴊᴇᴄᴛ', url=github_project)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/920475941946396673/649d4046150955e7ba1cddf18085b549.webp?size=4096')
        embed.add_field(
            name='ᴅᴇᴠᴇʟᴏᴘᴇʀ:',
            value=f"[1M65#8946]({owner_url})",
            inline=False
        )
        view = ui.View()
        view.add_item(ui.Button(label='ɢɪᴛʜᴜʙ', url=github_project, row=0))
        view.add_item(ui.Button(label='ᴋᴏ-ꜰɪ', url='https://www.youtube.com/watch?v=g97La0u55_g', row=0))

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: ValorantBot) -> None:
    await bot.add_cog(Admin(bot))
