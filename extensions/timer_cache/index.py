from discord.ext import tasks, commands
from discord import Interaction, SlashCommand
from index import MudaeBot
from extensions.timer_cache.timer_cleaner import get_timers
from components.state import Timer

import os
import asyncio
import time
import re
import json


class TimerCache(commands.Cog):
    def __init__(self, bot: MudaeBot):
        self.bot = bot

        self.timer_cache.start()

    def cog_unload(self):
        self.timer_cache.cancel()

    @tasks.loop(hours=2, reconnect=True)
    async def timer_cache(self):
        self.bot.logger.info("STARTING_TIMER_CACHE")

        channel = await self.bot.fetch_channel(os.getenv("SNIPE_CHANNEL_ID", None))
        timer_command_id = int(os.getenv("TIMER_COMMAND_ID", None))

        commands_list = [
            command
            async for command in channel.slash_commands(command_ids=[timer_command_id])
        ]

        if len(commands_list) == 0:
            self.bot.logger.error("$COMMAND_NOT_FOUND")
            return

        # Timer up command
        timer_up_command = next(
            command for command in commands_list if command.id == timer_command_id
        )

        timer_response = await get_timers(channel, timer_up_command)

        self.bot.logger.info("TIMER_CACHE_SUCCESS")

        self.bot.state.timer = Timer(timer_response)

    @timer_cache.before_loop
    async def before_timer_cache(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(5)


async def setup(bot: commands.Bot):
    await bot.add_cog(TimerCache(bot))
