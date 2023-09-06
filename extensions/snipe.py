from discord.ext import tasks, commands
import discord
import os
import re
import time
import json
from index import MudaeBot

from utils.catch_all import catch_all

pagination_regex = re.compile(r"\d+ / \d+")


class Snipe(commands.Cog):
    def __init__(self, bot: MudaeBot):
        self.bot = bot

        # Listen to on_message event
        self.bot.listen("on_message")(catch_all(self.snipe_tick))

        self.bot.logger.info("EXTENSION_LOADED_SNIPE")

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

        # Regex to check if there is a pagination in the footer
        footer_text = message.embeds[0].footer.text
        if footer_text and pagination_regex.search(footer_text):
            return False

        return True

    async def snipe_tick(self, message: discord.Message):
        if not self.roll_checker(message):
            return

        embed = message.embeds[0]

        # Check if the roll has a kakera claim
        kakera_emoji_list = json.loads(os.getenv("KAKERA_EMOJI_LIST"))

        if message.components != [] and message.components[0].children != []:
            kakera_emoji = message.components[0].children[0].emoji.name
            if kakera_emoji in kakera_emoji_list:
                # Click the kakera claim button
                self.bot.logger.info("KAKERA_SNIPER_CLAIM_SUCCESS")

                await message.components[0].children[0].click()
                return

        # timeout check
        if time.time() < self.bot.state.timeout:
            self.bot.logger.info("CLAIM_BLOCKED_TIMEOUT")
            return

        # Check if the roll is from a wishlist
        # If not, check if the kakera value is above the threshold
        if "Desejado por" not in message.content:
            split_description = embed.description.split("\n")

            if len(split_description) < 2:
                return

            core_description_split = split_description[1].split("**")

            if len(core_description_split) < 2:
                return

            kakera_value = core_description_split[1]

            if int(kakera_value) < int(os.getenv("KAKERA_THRESHOLD")):
                return

        else:
            if message.components != [] and message.components[0].children != []:
                await message.components[0].children[0].click()
                self.bot.logger.info("WISHLIST_SNIPER_CLAIM_SUCCESS")
                return

        self.bot.logger.info("KAKERA_SNIPER_SUCCESS")
        await message.add_reaction("👀")


async def setup(bot: commands.Bot):
    await bot.add_cog(Snipe(bot))
