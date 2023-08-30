from discord.ext import tasks, commands
import os
import asyncio
from index import MudaeBot


class RollMarry(commands.Cog):
    def __init__(self, bot: MudaeBot):
        self.bot = bot
        self.roll.start()

        self.bot.logger.info("EXTENSION_LOADED", extra={"extension": "roll_marry"})

    @tasks.loop(seconds=10)
    async def roll(self):
        if self.bot.state.timer.rolls_left == 0:
            return

        channel = await self.bot.fetch_channel(os.getenv("SNIPE_CHANNEL_ID", None))

        async def send_marry_roll(channel):
            await channel.send("$m")

        for _ in range(self.bot.state.timer.rolls_left):
            self.bot.logger.info("SENDING_MARRY_COMMAND")

            await asyncio.sleep(2)

            self.bot.loop.create_task(send_marry_roll(channel))

            self.bot.state.timer.rolls_left -= 1

        self.bot.logger.info("ROLL_SUCCESS")

    @roll.before_loop
    async def before_roll(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(RollMarry(bot))
