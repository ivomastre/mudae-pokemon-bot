import asyncio
import logging
import logging.handlers
import os
import discord
import json


from components.state import State
from typing import List, Optional
from discord.ext import commands
from dotenv import load_dotenv


class MudaeBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        logger: logging.Logger,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions
        self.logger = logger
        self.state = State()

    async def setup_hook(self) -> None:
        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        for extension in self.initial_extensions:
            await self.load_extension("extensions." + extension)

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")


async def main():
    logger = logging.getLogger("MUDAE")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    discord.utils.setup_logging(formatter=formatter, handler=handler, root=False)

    load_dotenv()  # take environment variables from .env.

    exts = json.loads(os.getenv("EXTENSION_LIST"))

    async with MudaeBot(
        commands.when_mentioned_or(os.getenv("PREFIX", "?")),
        initial_extensions=exts,
        logger=logger,
        self_bot=True,
    ) as bot:
        await bot.start(os.getenv("TOKEN", ""))


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
if __name__ == "__main__":
    asyncio.run(main())
