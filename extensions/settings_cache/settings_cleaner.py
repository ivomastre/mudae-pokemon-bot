from discord.ext import tasks, commands
from discord import Message, SlashCommand, TextChannel
import os
import asyncio
import time
import re
from index import MudaeBot

settings_highlight_regex = re.compile(r"\*\*(.+?)\*\*")


async def get_settings(channel: TextChannel, settings_command: SlashCommand):
    settings_response = await settings_command()

    settings_interaction_id = settings_response.id

    def check_integration(message):
        if not message.interaction:
            return False

        return message.interaction.id == settings_interaction_id

    settings_message_list = [
        message async for message in channel.history() if check_integration(message)
    ]

    if len(settings_message_list) == 0:
        return None

    settings_message = settings_message_list[0]

    clean_settings = settings_response_cleaner(settings_message)

    return clean_settings


def settings_response_cleaner(settings_message: Message):
    highlight_points = settings_highlight_regex.findall(settings_message.content)

    clean_settings = {
        "marry_claim_reset": int(highlight_points[3]) * 60,
        "exact_minute_claim_reset": int(highlight_points[4]),
    }

    return clean_settings
