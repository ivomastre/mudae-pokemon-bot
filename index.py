import asyncio
import logging
import logging.handlers
import os

from typing import List, Optional

import discord
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

    load_dotenv()  # take environment variables from .env.

    exts = ["pokemon", "autorelease", "snipe"]

    async with MudaeBot(
        commands.when_mentioned,
        initial_extensions=exts,
        logger=logger,
    ) as bot:
        await bot.start(os.getenv("TOKEN", ""))


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
asyncio.run(main())
