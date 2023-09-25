from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
مرحبا عزيزي {}

**- يعمل البوت بسهولة وبكل بساطة **
**- بوت خاص باستخراح جلسات تليثون وبروجرام **
  
**اضغط على بدء الاستخراج للإستخراج**
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton("• بدء الاستخراج •", callback_data="generate")],
        [InlineKeyboardButton(text="🏠 القائمة 🏠", callback_data="home")]
    ]

    generate_button = [
        [InlineKeyboardButton("• بدء الإستخراج •", callback_data="generate")]
    ]

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("• بدء الاستخراج •", callback_data="generate")],
        [InlineKeyboardButton("🇾🇪 المطور 🇾🇪", url="https://t.me/tzypis")],
        [
            InlineKeyboardButton("الاوامر ❔", callback_data="help"),
            InlineKeyboardButton("🤖 About 🤖", callback_data="about")
        ],
        [InlineKeyboardButton("• قناة السورس •", url="https://t.me/Mlze1bot")],
    ]

    # Help Message
    HELP = """
👇🏻 **Perintah yang tersedia** 👇🏻

/about - Tentang Bot ini
/help - Pesan ini
/start - Mulai Bot
/generate - Mulai Generating Session
/cancel - Membatalkan proses
/restart - Membatalkan proses
"""

    # About Message
    ABOUT = """
**Tentang Bot ini** 

Sebuah telegram bot untuk mengambil pyrogram dan telethon String Session

Grup Support : [Userbot Telegram](https://t.me/UserbotTelegramSupport)

Kerangka : [Pyrogram](docs.pyrogram.org)

Bahasa : [Python](www.python.org)

Developer : @tzypis
    """
