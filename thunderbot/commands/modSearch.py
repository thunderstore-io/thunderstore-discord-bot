from discord.ext import commands
from thunderbot.tools import settings
from fuzzywuzzy import process

class ModSearch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Search", "s", "S"], brief="Searches for a package on thunderstore and sends the url",
                      help="Usage !search (package)")
    async def search(self, ctx, *, arg):
        await ctx.trigger_typing()
        NAME_LIST = settings.NAME_LIST
        PACKAGE_LIST = settings.PACKAGE_DICT

        query = arg
        best = process.extractOne(query, NAME_LIST)
        if best is None:
            await ctx.send(f'Package ({arg}) not found')
        else:
            dex = NAME_LIST.index(best[0])
            url = PACKAGE_LIST[dex]["package_url"]
            await ctx.send(url)


def setup(client):
    client.add_cog(ModSearch(client))
