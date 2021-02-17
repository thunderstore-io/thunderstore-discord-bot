import asyncio
import os
from discord.ext import commands, tasks
import requests
import jwt
from thunderbot.tools.stringDecode import base64_decode
import json
from fuzzywuzzy import process

API_KEY = os.getenv("THUNDERSTORE_API_KEY_ID")
USER_AGENT = 'Mozilla/5.0'
url = os.getenv("THUNDERSTORE_API_URL")
USER_KEY = base64_decode(os.getenv("THUNDERSTORE_API_SECRET"))
USER_ALGORITHM = os.getenv("THUNDERSTORE_API_ALGORITHM")
PACKAGE_REFRESH_TIME = os.getenv("PACKAGE_REFRESH_TIME")
NAME_LIST = []


def thunderstore_get(packageName, userid):
    data = jwt.encode(
        payload={"package": packageName, "user": userid},
        key=USER_KEY,
        algorithm=USER_ALGORITHM,
        headers={"kid": API_KEY},

    )
    header = {"content-type": "application/jwt"}
    response = requests.post(url + "/v1/bot/deprecate-mod/", data, headers=header)
    print(url + "/v1/bot/deprecate-mod/")
    return response


class Deprecate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def deprecate(self, ctx, *, arg):

        query = arg
        best = process.extractOne(query, NAME_LIST, score_cutoff=95)
        if best is None:
            await ctx.send(f'Package ({arg}) not found')
        else:
            num = NAME_LIST.index(best[0])

            checkmsg = await ctx.send(f'react with :white_check_mark: to depricate ( {best[0]} ) or'
                                      f' :negative_squared_cross_mark:  to cancel', delete_after=80)

            await checkmsg.add_reaction('✅')
            await checkmsg.add_reaction('❎')

            def check(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎')

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('Command timed out', delete_after=20)
                return
            if str(reaction.emoji) == '❎':
                await ctx.send('Canceled', delete_after=20)
                return

            try:
                r = thunderstore_get(best[0], ctx.author.id)
                if r.status_code != 200:
                    await ctx.send(f"<@!{ctx.author.id}>"
                                   "\n Command should be: !deprecate {Package Full Name} "
                                   "\nExample: !deprecate \"bbepis-BepInExPack\" "
                                   "\nAn error occurred while executing the command. "
                                   "\nDetails: "
                                   f"\n``` {r.content}```")

                else:
                    await ctx.send(f"<@!{ctx.author.id}>\n"
                                   f"Package ({best[0]}) deprecated successfully!")
            except:
                await ctx.send("error with deprecate command")
                print("error with deprecate command")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'logged in as {self.client.user}')
        self.getlist.start()

    @commands.command()
    async def reloadlist(self, ctx):
        await self.getlist()
        await ctx.send(f'Package list reloaded')

    @tasks.loop(minutes=float(PACKAGE_REFRESH_TIME))
    async def getlist(self):

        header = {"content-type": "application/json"}
        response = requests.get(url + "/v1/package/", headers=header)
        API_LIST = json.loads(response.content)
        for dict in API_LIST:
            NAME_LIST.append(dict["full_name"])


def setup(client):
    client.add_cog(Deprecate(client))
