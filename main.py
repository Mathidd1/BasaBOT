import discord
from discord.ext import commands
import os
from help_cog import help_cog
from music_cog import music_cog
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= '$', intents= intents)

bot.remove_command("help")

async def setup_bot(bot):
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))
asyncio.run(setup_bot(bot))

bot.run()