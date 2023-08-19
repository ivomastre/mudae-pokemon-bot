from discord.ext import tasks, commands
import os
import asyncio


class AutoRelease(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.job.start()
        self.bot = bot
        self.pokemon = self.bot.get_cog("Pokemon")

    def cog_unload(self):
        self.job.cancel()

    @tasks.loop(hours=11)
    async def job(self):
        channel = await self.bot.fetch_channel(os.getenv("ARL_CHANNEL_ID", None))

        async def send_pokemon_release(bot, channel):
            await asyncio.sleep(20)

            bot.logger.info("Sending $arl")
            await channel.send("$arl")

        self.bot.loop.create_task(send_pokemon_release(self.bot, channel))

        self.bot.logger.info("Waiting for Mudae response")

        try:
            mudae_response = await self.bot.wait_for(
                "message",
                check=lambda m: (
                    m.author.id == int(os.getenv("MUDAE_ID"))
                    and m.channel.id == int(channel.id)
                    # arl response detection
                    and (
                        "Rocket casino" in m.content
                        or "You need at least one releasable" in m.content
                    )
                ),
                timeout=60 * 2,
            )

        except asyncio.TimeoutError:
            self.bot.logger.error("Mudae response timed out")
            return

        print(mudae_response.content)
        if "Rocket casino" in mudae_response.content:
            # string structure: **integer** Pokemon given

            while True:
                catcher_response = await asyncio.wait_for(
                    self.pokemon.catcher(), timeout=60 * 60
                )

                if catcher_response["empty"]:
                    break

        self.bot.logger.info("AutoRelease successful")


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoRelease(bot))
