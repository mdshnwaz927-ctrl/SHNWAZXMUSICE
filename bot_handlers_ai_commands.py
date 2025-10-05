from pyrogram import Client, filters
from bot.core.ai_recommendation import recommend_song, analyze_mood, transcribe_audio, identify_song

@Client.on_message(filters.command(["recommend", "generate"]))
async def recommend_handler(client, message):
    query = " ".join(message.command[1:])
    await recommend_song(message, query)

@Client.on_message(filters.command("identify"))
async def identify_handler(client, message):
    if not message.audio and not message.voice:
        await message.reply("Please send an audio file to identify.")
        return
    await identify_song(message)

@Client.on_message(filters.command("transcribe"))
async def transcribe_handler(client, message):
    if not message.audio and not message.voice:
        await message.reply("Please send an audio file to transcribe.")
        return
    await transcribe_audio(message)

@Client.on_message(filters.command("mood"))
async def mood_handler(client, message):
    await analyze_mood(message)

# ... more handlers as needed