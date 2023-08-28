from discord.ext import tasks, commands
import os
import asyncio
import time


class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def alert_finished_timeout(self, user_id: int):
        # Ping the user
        await self.bot.get_channel(int(os.getenv("SNIPE_CHANNEL_ID"))).send(
            f"<@{user_id}> acabou o timeout"
        )

    @commands.command()
    async def timeout(self, ctx: commands.Context):
        if ctx.channel.id != int(os.getenv("SNIPE_CHANNEL_ID")):
            return

        timeout_timer = int(os.getenv("TIMEOUT_TIMER"))

        # 1 minutes timeout
        next_timeout = time.time() + timeout_timer

        self.bot.state.timeout = next_timeout

        # Send a message to the user
        await ctx.reply("blz")

        # Wait for the timeout to finish
        # And then ping the user
        await asyncio.sleep(timeout_timer)
        asyncio.create_task(self.alert_finished_timeout(ctx.author.id))


async def setup(bot: commands.Bot):
    await bot.add_cog(Timeout(bot))
