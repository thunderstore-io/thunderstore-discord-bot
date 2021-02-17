import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import logging


intents = discord.Intents.all()
load_dotenv()

client = commands.Bot(command_prefix="!",intents = intents)
token = os.getenv("DISCORD_TOKEN")




print(token)

@client.command(pass_context=True)
async def load(ctx, extension):
    client.load_extension(f'commands.{extension}')


async def unload(ctx, extension):
    client.unload_extension(f'commands.{extension}')


for filename in os.listdir('commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

logging.basicConfig(level=logging.INFO)




client.run(token)
