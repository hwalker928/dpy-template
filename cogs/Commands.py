import discord
from discord.ext import commands
from datetime import datetime
from discord.utils import get
import aiohttp
from pathlib import Path
import asyncio

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def embed(self,ctx,title,description):
        """Creates an embed."""
        embed=discord.Embed(title=f"{title}", description=description, color=ctx.guild.me.color)
        embed.set_footer(text=f"{ctx.guild.name} • Posted by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["r", "rl", "pull", "sync"])
    @commands.is_owner()
    async def reload(self, ctx):
        cogs = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in cogs:
            try:
                self.bot.reload_extension(f'cogs.{extension}')
            except:
                pass
        await ctx.send("Reloaded.")

def setup(bot):
    bot.add_cog(Commands(bot))