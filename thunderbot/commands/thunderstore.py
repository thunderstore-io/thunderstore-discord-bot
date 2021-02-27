import discord
from discord.ext import commands, tasks
import requests
import json
from thunderbot.tools import settings


class Thunderstore(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'logged in as {self.client.user}')
        self.getlist.start()

    @commands.command(aliases=["Reloadpackages","Reload","reload", "R", "r"], brief="Reloads the package cache ",
                      help="Usage !reloadpackages")
    async def reloadpackages(self, ctx):
        await ctx.trigger_typing()
        await self.getlist()
        await ctx.send(f'Package list reloaded')

    @tasks.loop(minutes=float(settings.PACKAGE_REFRESH_TIME))
    async def getlist(self):
        await self.client.change_presence(activity=discord.Game(f'Refreshing Packages'))
        header = {"content-type": "application/json"}
        response = requests.get(settings.URL + "/v1/package/", headers=header)
        PACKAGE_LIST = json.loads(response.content)
        settings.PACKAGE_LIST = PACKAGE_LIST
        settings.NAME_LIST = []
        for d in PACKAGE_LIST:
            settings.NAME_LIST.append(d["full_name"])
        await self.client.change_presence(activity=discord.Game(f'{len(settings.NAME_LIST)} total packages'))


def setup(client):
    client.add_cog(Thunderstore(client))
