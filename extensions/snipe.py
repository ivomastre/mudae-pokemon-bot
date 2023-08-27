from discord.ext import tasks, commands
import discord
import os
import re

pagination_regex = re.compile(r"\d+ / \d+")


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Register an event
        self.bot.event(self.on_message)

    def roll_checker(self, message: discord.Message):
        if (
            message.author.id != int(os.getenv("MUDAE_ID"))
            or message.author.id == self.bot.user.id
        ):
            return False

        if not message.embeds:
            return False

        if message.channel.id != int(os.getenv("SNIPE_CHANNEL_ID")):
            return False

        if not message.embeds[0].image or not message.embeds[0].author:
            return False

        # Check if theres a pagination in the footer

        if pagination_regex.search(message.embeds[0].footer.text):
            return False

        return True

    async def on_message(self, message: discord.Message):
        if not self.roll_checker(message):
            return

        embed = message.embeds[0]

        kakera_value = embed.description.split("\n")[1].split("**")[1]
        if int(kakera_value) < int(os.getenv("KAKERA_THRESHOLD")):
            return

        self.bot.logger.info("KAKERA_SNIPER_SUCCESS")
        await message.add_reaction("👀")


async def setup(bot: commands.Bot):
    await bot.add_cog(Snipe(bot))
