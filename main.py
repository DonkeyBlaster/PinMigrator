import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
pins_channel: int = int(os.getenv("PINS"))

intents = discord.Intents.default()
intents.messages = True
intents.typing = False
intents.presences = False

client: discord.Client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for pins"))


@client.event
async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):

    if str(reaction.emoji) != "📌" and str(reaction.emoji) != "⭐":
        return

    migration_channel: discord.TextChannel = client.get_channel(pins_channel)
    if migration_channel is None:
        print("Could not find pins channel")
        return

    message: discord.Message = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)
    await migration_channel.send(embed=generate_embed(message))
    await message.add_reaction("✅")


@client.event
async def on_raw_message_edit(payload: discord.RawMessageUpdateEvent):
    migration_channel: discord.TextChannel = client.get_channel(pins_channel)
    if migration_channel is None:
        print("Could not find pins channel")
        return

    message: discord.Message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if message.pinned:
        await migration_channel.send(embed=generate_embed(message))
        await message.unpin()
        await message.add_reaction("✅")


def generate_embed(message: discord.Message) -> discord.Embed:
    embed: discord.Embed = discord.Embed(color=0x2f3136)
    embed.add_field(name=f"{message.jump_url}", value=message.content, inline=False)
    if len(message.attachments) > 0:
        embed.add_field(name="Attachments",
                        value="\n".join([attachment.url for attachment in message.attachments]), inline=False)
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar)
    return embed


client.run(TOKEN)
