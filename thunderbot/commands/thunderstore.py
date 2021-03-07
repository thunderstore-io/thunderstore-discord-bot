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

    @commands.command(aliases=["Reloadpackages", "Reload", "reload", "R", "r"], brief="Reloads the package cache ",
                      help="Usage !reloadpackages")
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
                response = requests.get(settings.SER_PREF[ser][1] + "/v1/package/", headers=header)
                package_list = json.loads(response.content)
                settings.SER_PREF[ser][2] = package_list
                settings.SER_PREF[ser][3] = []

                for d in package_list:
                    settings.SER_PREF[ser][3].append(d["full_name"])
                total += len(settings.SER_PREF[ser][3])
        except:
            print("Error with package refresh")
            await self.client.change_presence(activity=discord.Game(f'Cannot connect to Thunderstore'))

        await self.client.change_presence(activity=discord.Game(f'{total} total packages'))


def setup(client):
    client.add_cog(Thunderstore(client))
