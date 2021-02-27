import asyncio
from discord.ext import commands
import requests
import jwt
from thunderbot.tools import settings
from fuzzywuzzy import process


def thunderstore_get(packagename, userid):
    data = jwt.encode(
        payload={"package": packagename, "user": userid},
        key=settings.USER_KEY,
        algorithm=settings.USER_ALGORITHM,
        headers={"kid": settings.API_KEY},

    )
    header = {"content-type": "application/jwt"}
    response = requests.post(settings.URL + "/v1/bot/deprecate-mod/", data, headers=header)
    return response


class Deprecate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Deprecate", "d", "D"], brief="Deprecates a package on thunderstore",
                      help="Usage !deprecate (package)")
    async def deprecate(self, ctx, *, arg):
        await ctx.trigger_typing()
        NAME_LIST = settings.NAME_LIST
        PACKAGE_LIST = settings.PACKAGE_LIST

        query = arg
        best = process.extractOne(query, NAME_LIST)
        if best is None:
            await ctx.send(f'Package ({arg}) not found')
        else:
            dex = NAME_LIST.index(best[0])
            url = PACKAGE_LIST[dex]["package_url"]
            checkmsg = await ctx.send(f'Deprecate ( {url} ) ?')

            await checkmsg.add_reaction('✅')
            await checkmsg.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('Command timed out')
                return
            if str(reaction.emoji) == '❌':
                await ctx.send('Canceled')
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


def setup(client):
    client.add_cog(Deprecate(client))
