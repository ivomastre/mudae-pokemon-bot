from discord.ext import tasks, commands
import os
import asyncio


class Pokemon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.catcher.start()
        self.bot = bot

    def cog_unload(self):
        self.catcher.cancel()

    @tasks.loop(hours=2)
    async def catcher(self):
        channel = await self.bot.fetch_channel(os.getenv("CHANNEL_ID", None))

        async def send_pokemon_catch(bot, channel):
            await asyncio.sleep(2)

            bot.logger.info("Sending $p")
            await channel.send("$p 25")

        self.bot.loop.create_task(send_pokemon_catch(self.bot, channel))

        self.bot.logger.info("Waiting for Mudae response")

        try:
            mudae_response = await self.bot.wait_for(
                "message",
                check=lambda m: (
                    m.author.id == int(os.getenv("MUDAE_ID"))
                    and m.channel.id == int(channel.id)
                ),
                timeout=60 * 2,
            )

        except asyncio.TimeoutError:
            self.bot.logger.error("Mudae response timed out")
            return

        self.bot.logger.info("Pokemon command successful")

        # Empty pokeroll detection

        if "Remaining time before your next $p" in mudae_response.content:
            self.bot.logger.info("Empty pokeroll detected")
            return {
                "empty": True,
                "remaining_time": (
                    mudae_response.content.split("Remaining time before your next $p:")[
                        1
                    ].strip()
                ),
                "success": True,
            }

        return {
            "empty": False,
            "success": True,
        }


async def setup(bot: commands.Bot):
    await bot.add_cog(Pokemon(bot))
