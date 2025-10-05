import os, asyncio, yt_dlp, json
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("novabeat_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# In-memory data
search_cache, queue, playlists, roles = {}, {}, {}, {}

# Multi-language stub
MESSAGES = {
    "en": {"no_query": "❗ Please provide a song name or link.", "playing": "🎶 Now playing"},
    "es": {"no_query": "❗ Por favor, proporciona una canción o enlace.", "playing": "🎶 Reproduciendo"},
}
def get_msg(chat_id, key):  # You could expand this to detect lang per user/chat
    return MESSAGES["en"][key]

# Fast download
async def fast_download(query):
    if query in search_cache and (asyncio.get_event_loop().time() - search_cache[query]['time'] < 300):
        return search_cache[query]['path']
    loop = asyncio.get_event_loop()
    def download():
        ydl_opts = {"format": "bestaudio/best", "outtmpl": "downloads/%(title)s.%(ext)s", "quiet": True, "noplaylist": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            return ydl.prepare_filename(info)
    audio_path = await loop.run_in_executor(None, download)
    search_cache[query] = {"path": audio_path, "time": loop.time()}
    return audio_path

START_MESSAGE = """
👋 Hello, {name}!
🎵 Welcome to NovaBeat – AI-powered all-in-one music companion (2025)!
Try /play, /queue, /skip, /recommend, /remix, /lyrics, /party, /quiz, /trendify
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("▶️ Start Listening", callback_data="start_listening"),
     InlineKeyboardButton("🌎 Language", callback_data="change_language")],
    [InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
])

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    name = message.from_user.first_name if message.from_user else "there"
    await message.reply(START_MESSAGE.format(name=name), reply_markup=START_BUTTONS, disable_web_page_preview=True)

@app.on_message(filters.command("play"))
async def play_handler(client, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply(get_msg(message.chat.id, "no_query"))
        return
    await message.reply("🔍 Searching and downloading your song, please wait...")
    try:
        audio_path = await fast_download(query)
        queue.setdefault(message.chat.id, []).append(audio_path)
        await message.reply_audio(audio_path, caption=f"{get_msg(message.chat.id, 'playing')}: {query}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@app.on_message(filters.command("queue"))
async def queue_handler(client, message):
    qlist = queue.get(message.chat.id, [])
    if not qlist:
        await message.reply("Queue is empty!")
        return
    await message.reply("Current queue:\n" + "\n".join([os.path.basename(p) for p in qlist]))

@app.on_message(filters.command("skip"))
async def skip_handler(client, message):
    qlist = queue.get(message.chat.id, [])
    if qlist:
        skipped = qlist.pop(0)
        await message.reply(f"Skipped {os.path.basename(skipped)}.")
        if qlist:
            await message.reply_audio(qlist[0], caption="Next song:")
    else:
        await message.reply("Queue is empty!")

@app.on_message(filters.command("saveplaylist"))
async def save_playlist_handler(client, message):
    name = " ".join(message.command[1:]) or "default"
    playlists[name] = queue.get(message.chat.id, []).copy()
    await message.reply(f"Playlist '{name}' saved!")

@app.on_message(filters.command("loadplaylist"))
async def load_playlist_handler(client, message):
    name = " ".join(message.command[1:]) or "default"
    pl = playlists.get(name)
    if pl:
        queue[message.chat.id] = pl.copy()
        await message.reply(f"Loaded playlist '{name}'!")
    else:
        await message.reply("Playlist not found.")

@app.on_message(filters.command("lyrics"))
async def lyrics_handler(client, message):
    song = " ".join(message.command[1:]) or "unknown"
    await message.reply(f"Lyrics for {song} (feature coming soon!)")

@app.on_message(filters.command("recommend"))
async def recommend_handler(client, message):
    await message.reply("🤖 AI Recommendation feature coming soon!")

@app.on_message(filters.command("trendify"))
async def trendify_handler(client, message):
    await message.reply("Trending charts:\n1. Song A\n2. Song B\n3. Song C")

@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    if data == "start_listening":
        await callback_query.message.reply("Type /play [song name] to start!")
    elif data == "change_language":
        await callback_query.message.reply("🌎 Language selection coming soon!")
    elif data == "settings":
        await callback_query.message.reply("⚙️ Settings panel coming soon!")

if __name__ == "__main__":
    app.run()