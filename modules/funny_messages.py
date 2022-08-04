import random
from os.path import dirname, basename, isfile, join
import discord

funny_messages = []


def init():
    global funny_messages

    text_file = open(
        join(dirname(__file__), "funny_messages.dat"), "r", encoding="utf-8"
    )
    funny_messages = text_file.readlines()
    text_file.close()


async def execute_command(client, message):
    global funny_messages
    print(message)

    if isinstance(message.channel, discord.TextChannel):
        if message.channel.name != "červený-trpaslík":
            return

    if isinstance(message.channel, discord.DMChannel):
        # private channel
        pass

    text = random.choice(funny_messages)
    await message.channel.send(text)


def register(main):
    main["funny_messages"] = {
        "cmd": "$funny",
        "description": "Send funny message",
        "execute": execute_command,
        "init": init,
    }
