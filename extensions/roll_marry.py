from discord.ext import tasks, commands
import os
import asyncio
from index import MudaeBot

import time


class RollMarry(commands.Cog):
    def __init__(self, bot: MudaeBot):
        self.bot = bot
        self.roll.start()

        self.bot.logger.info("EXTENSION_LOADED_ROLL_MARRY")

    @tasks.loop(seconds=10)
    async def roll(self):
        # Update next roll time
        if (
            self.bot.state.timer.next_roll_time > 0
            and self.bot.state.timer.next_roll_time < time.time()
        ):
            self.bot.state.timer.next_roll_time = (
                self.bot.state.settings.marry_claim_reset + time.time() + 120
            )

            self.bot.logger.info(
                f"NEXT_ROLL_TIME_UPDATED: {self.bot.state.timer.next_roll_time}"
            )

            if self.bot.state.timer.rolls_left == 0:
                self.bot.state.timer.rolls_left = self.bot.state.settings.marry_rolls

                self.bot.logger.info(
                    f"ROLLS_LEFT_UPDATED: {self.bot.state.timer.rolls_left}"
                )

        # Check if rolls are available
        if self.bot.state.timer.rolls_left == 0:
            return

        channel = await self.bot.fetch_channel(os.getenv("SNIPE_CHANNEL_ID", None))

        for _ in range(self.bot.state.timer.rolls_left):
            self.bot.logger.info("SENDING_MARRY_COMMAND")

            await asyncio.sleep(5)

            try:
                await channel.send("$m")
            except Exception as e:
                self.bot.logger.error(f"SENDING_MARRY_COMMAND_FAILED: \n{e}")

            self.bot.state.timer.rolls_left -= 1

        self.bot.logger.info("ROLL_SUCCESS")

    @roll.before_loop
    async def before_roll(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(RollMarry(bot))
