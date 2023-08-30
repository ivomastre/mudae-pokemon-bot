from discord.ext import tasks, commands
from discord import Interaction, SlashCommand
from index import MudaeBot
from extensions.settings_cache.settings_cleaner import get_settings
from components.state import Settings


import os
import asyncio
import time
import re
import json


class SettingsCache(commands.Cog):
    def __init__(self, bot: MudaeBot):
        self.bot = bot

        self.settings_cache.start()

    def cog_unload(self):
        self.settings_cache.cancel()

    @tasks.loop(hours=11, reconnect=True)
    async def settings_cache(self):
        self.bot.logger.info("STARTING_SETTINGS_CACHE")

        channel = await self.bot.fetch_channel(os.getenv("SNIPE_CHANNEL_ID", None))
        settings_command_id = int(os.getenv("SETTINGS_COMMAND_ID", None))

        commands_list = [
            command
            async for command in channel.slash_commands(
                command_ids=[settings_command_id]
            )
        ]

        if len(commands_list) == 0:
            self.bot.logger.error("COMMAND_NOT_FOUND")
            return

        settings_command = next(
            command for command in commands_list if command.id == settings_command_id
        )

        settings_response = await get_settings(channel, settings_command)

        self.bot.logger.info("SETTINGS_CACHE_SUCCESS")

        self.bot.state.settings = Settings(settings_response)

    @settings_cache.before_loop
    async def before_settings_cache(self):
        await self.bot.wait_until_ready()

        await asyncio.sleep(15)


async def setup(bot: commands.Bot):
    await bot.add_cog(SettingsCache(bot))
