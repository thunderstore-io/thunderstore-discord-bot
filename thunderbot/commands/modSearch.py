from discord.ext import commands
from thunderbot.tools import settings
from fuzzywuzzy import process

class ModSearch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Search", "s", "S"], brief="Searches for a package on thunderstore and sends the url",
                      help="Usage !search (package)")
    async def search(self, ctx, *, arg):
        if ctx.guild is None:
            await ctx.send("Please use command in a comunity server")
            return
        elif ctx.guild.id not in settings.SER_PREF:
            await ctx.send("Please use command in a comunity server")
            return

        await ctx.trigger_typing()
        NAME_LIST = settings.SER_PREF[ctx.guild.id][3]
        PACKAGE_DICT = settings.SER_PREF[ctx.guild.id][2]

        query = arg
        best = process.extractOne(query, NAME_LIST)
        if best is None:
            await ctx.send(f'Package ({arg}) not found')
        else:
            dex = NAME_LIST.index(best[0])
            url = PACKAGE_DICT[dex]["package_url"]
            await ctx.send(url)


def setup(client):
    client.add_cog(ModSearch(client))
