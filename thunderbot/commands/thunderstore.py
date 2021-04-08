import aiohttp
import discord
from discord.ext import commands, tasks
import json
from thunderbot.tools import settings
import asyncio


class Thunderstore(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'logged in as {self.client.user}')
        self.getlist.start()

    @commands.command(aliases=["Reloadpackages", "Reload", "reload", "R", "r"], brief="Reloads the package cache ",
                      help="Usage !reloadpackages",hidden=True)
    async def reloadpackages(self, ctx):
        await ctx.trigger_typing()
        await self.getlist()
        await ctx.send(f'Package list reloaded')

    @tasks.loop(minutes=float(settings.PACKAGE_REFRESH_TIME))
    async def getlist(self):
        await self.client.change_presence(activity=discord.Game(f'Refreshing Packages'))
        total = 0
        header = {"content-type": "application/json"}
        try:
            for ser in settings.SER_PREF:

                async with aiohttp.ClientSession(loop=self.client.loop) as session:
                    async with session.get(settings.SER_PREF[ser][1] + "/v1/package/") as r:
                        response = await r.json()

                settings.SER_PREF[ser][2] = response
                settings.SER_PREF[ser][3] = []

                for d in response:
                    settings.SER_PREF[ser][3].append(d["full_name"])
                total += len(settings.SER_PREF[ser][3])
            await asyncio.sleep(0.005)
        except Exception as e:
            print("Error with package refresh")
            print(e)
            await self.client.change_presence(activity=discord.Game(f'Cannot connect to Thunderstore'))

        await self.client.change_presence(activity=discord.Game(f'{total} total packages'))


def setup(client):
    client.add_cog(Thunderstore(client))
