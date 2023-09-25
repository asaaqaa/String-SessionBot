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
        [InlineKeyboardButton("🇾🇪 المطور 🇾🇪", url="https://t.me/A_S_A_S_K")],
        [
            InlineKeyboardButton("الاوامر ❔", callback_data="help"),
            InlineKeyboardButton("🤖 معلومات 🤖", callback_data="about")
        ],
        [InlineKeyboardButton("• قناة السورس •", url="https://t.me/Mlze1bot")],
    ]

    # Help Message
    HELP = """
👇🏻 **اوامر البوت** 👇🏻

/about - لعرض معلومات البوت
/help - قائمة المساعدة
/start - أمر البدء
/generate - لبدء استخراج جلسات البوت
"""

    # About Message
    ABOUT = """
**معلومات قد تهمگ** 

**هاذا البوت عبارة بوت استخراج جلسات تليثون وجلسات بروجرام **

-قناة السورس : [قناة البوت](https://t.me/Mlze1bot)

موقع بروجرام : [Pyrogram](docs.pyrogram.org)

موقع تليثون : [Python](www.python.org)

المطور : @A_S_A_S_K
    """
