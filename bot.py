import os
import re

import discord
import kadal


class TachiBoti(discord.Client):
    def __init__(self):
        super().__init__()
        self.regex = re.compile(r"<(.+)>")
        self.klient = kadal.Klient(loop=self.loop)

    async def format_embed(self, name):
        try:
            manga = await self.klient.search_manga(name)
        except kadal.MediaNotFound:
            return

        title = manga.title.get('english') or manga.title.get('romaji') or manga.title.get('native')
        desc = "***" + ", ".join(manga.genres) + "***\n"
        desc += manga.description[:256 - len(desc) - 7] + f"[...]({manga.site_url})"
        e = discord.Embed(title=title, description=desc, color=0x4286f4)
        e.set_thumbnail(url=manga.cover_image)
        e.url = manga.site_url
        return e

    async def on_ready(self):
        print("Ready!")
        print(self.user.name)
        print(self.user.id)
        print("~-~-~-~-~")

    async def on_message(self, message):
        m = self.regex.match(message.clean_content)
        if m:
            embed = await self.format_embed(m.group(1))
            if not embed:
                return
            await message.channel.send(embed=embed)


bot = TachiBoti()
token = os.environ.get('TOKEN')
if token is None:
    with open("token") as f:
        token = f.readline()
bot.run(token)