from discord.ext import tasks, commands
from discord import Interaction, SlashCommand, TextChannel, Message
import os
import asyncio
import time
import re
from index import MudaeBot

from utils.time_utils import mudae_time_to_seconds

timer_highlight_regex = re.compile(r"\*\*(.+?)\*\*")


async def get_timers(channel: TextChannel, timer_up_command: SlashCommand):
    timer_response = await timer_up_command()

    timer_interaction_id = timer_response.id

    def check_integration(message):
        if not message.interaction:
            return False

        return message.interaction.id == timer_interaction_id

    timer_message_list = [
        message async for message in channel.history() if check_integration(message)
    ]

    if len(timer_message_list) == 0:
        return None

    timer_message = timer_message_list[0]

    clean_timer = timer_message_cleaner(timer_message)

    return clean_timer


def timer_message_cleaner(timer_message: Message):
    highlight_points = timer_highlight_regex.findall(timer_message.content)

    clean_timer = {
        "can_claim_marry": True,  # TODO: implement scraping of this value
        "claim_reset": mudae_time_to_seconds(highlight_points[1]),
        "rolls_left": int(highlight_points[2]),
        "rolls_reset": mudae_time_to_seconds(highlight_points[3]),
        "daily_reset": mudae_time_to_seconds(highlight_points[4]),
    }

    return clean_timer
