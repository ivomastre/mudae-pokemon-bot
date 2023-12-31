from discord.ext import tasks, commands
import os
import asyncio
import time
from index import MudaeBot


class Timeout(commands.Cog):
    def __init__(self, bot: MudaeBot):
        self.bot = bot
        self.bot.logger.info("EXTENSION_LOADED_TIMEOUT")

    @commands.command()
    async def timeout(self, ctx: commands.Context):
        if ctx.channel.id != int(os.getenv("SNIPE_CHANNEL_ID")):
            return

        timeout_timer = int(os.getenv("TIMEOUT_TIMER"))

        next_timeout = time.time() + timeout_timer

        self.bot.logger.info(f"TIMEOUT_COMMAND_RECEIVED {timeout_timer}")

        self.bot.state.timeout = next_timeout


async def setup(bot: commands.Bot):
    await bot.add_cog(Timeout(bot))
