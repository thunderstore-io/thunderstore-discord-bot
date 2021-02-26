import discord
import os
from discord.ext import commands
import logging
from thunderbot.tools import settings

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)


@client.command(pass_context=True,hidden=True)
async def load(ctx, extension):
    client.load_extension(f'thunderbot.commands.{extension}')


async def unload(ctx, extension):
    client.unload_extension(f'thunderbot.commands.{extension}')


for filename in os.listdir('thunderbot/commands'):
    if filename.endswith('.py'):
        client.load_extension(f'thunderbot.commands.{filename[:-3]}')

logging.basicConfig(level=logging.INFO)

client.run(settings.TOKEN)
