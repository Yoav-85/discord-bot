from AI_Image import ask_bot
from audio_helpers import is_supported_audio_extension, audio_to_text
import discord
import schedule
import os
from dotenv import load_dotenv
from datetime import datetime

from email_sender import EmailSender

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
# Set up the Discord client
discord_client = discord.Client(intents=intents)

SENDER_EMAIL_ADDRESS = os.getenv('SENDER_EMAIL_ADDRESS')
SENDER_EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD')
email_sender_client = EmailSender(SENDER_EMAIL_ADDRESS, SENDER_EMAIL_PASSWORD)

reports_list = []


async def mute(member: discord.Member):
    # Check if the user is in a voice channel
    if member.voice:
        await member.edit(mute=True)  # Mute the member


async def unmute(member: discord.Member):
    # Check if the user is in a voice channel
    if member.voice:
        await member.edit(mute=False)  # Unmute the member

async def Ban_Users(member, message):

    guild = message.guild
    if member:
        await guild.ban(member, reason="Banned by bot")
        await message.channel.send(f"{member.mention} has been banned.")
    else:
        await message.channel.send("User not found in the server.")


# Event when bot has connected
@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}')


async def download_attachment(attachment, output_filepath):
    await attachment.save(output_filepath)


def is_transcription_cursed(transcription: str) -> bool:
    cursed_words = ["bitch", "monkey", "nigga", "nigger", "asshole", "n i g g a", "n i g g e r"]
    return transcription.lower() in cursed_words


async def report_curse(message, transcription):
    await message.channel.send(f"{message.author} thats your last warning")
    body = f"{message.author} sent {transcription} in {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} "
    reports_list.append(body)


async def handle_command(command, message):
    if command == "mute me":
        await mute(message.author)
    elif command == "unmute me":
        await unmute(message.author)


# Event for receiving a message
@discord_client.event
async def on_message(message):
    # Ignore messages sent by the bot
    if message.author == discord_client.user:
        return

    # Check for audio attachments
    if not message.attachments:
        return

    for attachment in message.attachments:
        if not is_supported_audio_extension(attachment.filename):
            continue

        # Download the file
        audio_path = attachment
        audio_filename = "tmp_discord_attachment.ogg"
        await download_attachment(audio_path, audio_filename)

        # Convert audio to text
        transcription = audio_to_text(audio_filename)
        if is_transcription_cursed(transcription):
            await report_curse(message, transcription)
            await Ban_Users(message.author,message)

        if transcription.splitlines('chat G P T'):
             await send_response(transcription,message)

        await handle_command(transcription, message)

        # Delete the file after processing
        os.remove(audio_filename)


def report_to_receiver():
    receiver = os.getenv('RECEIVER_EMAIL_ADDRESS')

    email_body = 'This is your reports:\n'
    email_body += '\n'.join(reports_list)

    if not reports_list:
        email_body = 'There were no reports today'

    email_sender_client.send_email('daily_report', email_body, [receiver])
    reports_list.clear()

async def send_response(transcription, message):

    response = ask_bot(transcription)
    if len(response) > 2000:
        messages = split_message(response)
        for msg in messages:
            await message.channel.send(msg)
    await message.channel.send((response))

def split_message(content, max_length=2000):

    return [content[i:i+max_length] for i in range(0, len(content), max_length)]

def main():
    schedule.every().day.at("20:00").do(report_to_receiver)
    # Run the bot
    discord_client.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
