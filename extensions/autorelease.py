from discord.ext import tasks, commands
import os
import asyncio
from index import MudaeBot


class AutoRelease(commands.Cog):
    def __init__(self, bot: MudaeBot):
        self.job.start()
        self.bot = bot
        self.pokemon = self.bot.get_cog("Pokemon")

        self.bot.logger.info("EXTENSION_LOADED", extra={"extension": "autorelease"})

    def cog_unload(self):
        self.job.cancel()

    @tasks.loop(hours=11)
    async def job(self):
        channel = await self.bot.fetch_channel(os.getenv("ARL_CHANNEL_ID", None))

        async def send_pokemon_release(channel):
            await asyncio.sleep(20)

            self.bot.logger.info("SENDING_ARL_COMMAND")
            await channel.send("$arl")

        self.bot.loop.create_task(send_pokemon_release(channel))

        try:
            mudae_response = await self.bot.wait_for(
                "message",
                check=lambda m: (
                    m.author.id == int(os.getenv("MUDAE_ID"))
                    and m.channel.id == int(channel.id)
                    # arl response detection
                    and (
                        "Rocket" in m.content
                        or "duplicado para este comando" in m.content
                    )
                ),
                timeout=60 * 2,
            )

        except asyncio.TimeoutError:
            self.bot.logger.error("MUDAE_RESPONSE_TIMED_OUT")
            return

        if "Rocket casino" in mudae_response.content:
            while True:
                catcher_response = await asyncio.wait_for(
                    self.pokemon.catcher(), timeout=60 * 60
                )

                if catcher_response["empty"]:
                    break

        self.bot.logger.info("AUTORELEASE_SUCCESS")

    @job.before_loop
    async def before_job(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoRelease(bot))
