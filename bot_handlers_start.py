from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_MESSAGE = """
👋 Hello, {name}!

🎵 Welcome to **NovaBeat** – Your AI-powered all-in-one music companion for Telegram (2025 Edition)!

✨ **What can I do?**
— Stream music from YouTube, Spotify, Deezer, Apple Music & more  
— Play in groups, channels, or private chats  
— Inline search, direct play, instant downloads  
— Queue, playlist, lyrics, effects, polls, party mode  
— AI music recommendations, auto DJ, trending charts  
— Song ID, mood analysis, transcription, smart remix & covers  
— Custom commands, multi-language, emoji reactions, visual menus  
— Voice & video chat integration, custom welcome music  
— 🚦 Multi-admin, anti-spam, and privacy controls

🤖 **Try these commands**:
`/play [song or link]`  •  `/recommend [mood]`  •  `/remix nightcore`  
`/queue`  •  `/lyrics`  •  `/compose [theme]`  •  `/identify`  
`/party`  •  `/quiz [artist]`  •  `/trendify`  •  `/volume 150`  
`/help` for the full command list

🌐 **Powered by Next-Gen AI**  
— Smart suggestions, auto-play, conversational assistant  
— Cross-platform sync, advanced audio effects, rich visuals

🧑‍💻 **Ready to drop the beat?**  
Type `/play` or tap the button below to begin your music journey!

NovaBeat adapts to your taste, mood, and party vibe.  
Your playlist, your world, your AI DJ.
"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("▶️ Start Listening", callback_data="start_listening"),
            InlineKeyboardButton("🌎 Language", callback_data="change_language"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
        ]
    ]
)

@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    name = message.from_user.first_name if message.from_user else "there"
    await message.reply(
        START_MESSAGE.format(name=name),
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True
    )