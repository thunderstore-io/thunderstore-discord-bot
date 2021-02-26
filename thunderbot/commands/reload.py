import os
from discord.ext import commands


class Reload(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def reloadcommands(self, ctx):
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                self.client.reload_extension(f'commands.{filename[:-3]}')
                await ctx.send(f'reloaded {filename[:-3]}')

    @commands.command(hidden=True)
    async def ping(self, ctx):
        await ctx.send("pong")


def setup(client):
    client.add_cog(Reload(client))
