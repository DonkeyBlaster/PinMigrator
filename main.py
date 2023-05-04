import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
watching_channel: int = int(os.getenv("WATCHING"))
pins_channel: int = int(os.getenv("PINS"))

client: discord.Client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="for pins in #general"))


@client.event
async def on_message(message: discord.Message):
    # why is this event required for the on_message_edit event to trigger???
    pass


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    print("Message edited")
    if (before.channel.id != watching_channel) or (after.channel.id != watching_channel):
        return

    if not before.pinned and after.pinned:  # message was pinned
        await after.unpin(reason="Pin migrated to pins channel")
        await after.add_reaction("📌")

        migration_channel: discord.TextChannel = client.get_channel(pins_channel)
        if migration_channel is None:
            print("Could not find pins channel")
            return

        embed: discord.Embed = discord.Embed(title="Pinned Message", color=0x2f3136)
        embed.add_field(name="Content", value=after.content, inline=False)
        if len(after.attachments) > 0:
            embed.add_field(name="Attachments",
                            value="\n".join([attachment.url for attachment in after.attachments]), inline=False)
        embed.set_author(name=after.author.display_name, icon_url=after.author.avatar)
        embed.set_footer(
            text=f"[Link]({after.jump_url})")
        await migration_channel.send(embed=embed)


client.run(TOKEN)
