from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

ERROR_MESSAGE = "Oops! Pengecualian terjadi ! \n\n**Error** : {} " \
            "\n\nTolong Laporan ke @UserbotTelegramSupport jika eror " \
            "informasi sensitif dan Anda jika ingin melaporkan ini sebagai " \
            "pesan kesalahan ini tidak dicatat oleh kami !"


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "**-أختر تلثيون لاستخراج جلسة يوزر بوت او أختار بروجرام لاستخراج جلسة مساعد ميوزك",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("بروجــرام", callback_data="pyrogram"),
            InlineKeyboardButton("تيلــثيون", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("__Memulai {} Session Generation...__".format("Telethon" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'Tolong Kirimkan  `API_ID` Anda Disini', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('API_ID Tidak Benar , Tolong mulai ulang generating session lagi', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'Tolong Kirimkan `API_HASH` Anda Disini', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'Sekarang Kirimkan Nomor Telepon Anda Dengan Kode Nomor Negara\n\n**Contoh :** `+628xxxxxxx`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("```Mengirimkan Kode OTP...```")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`API_ID` dan `API_HASH` masih salah , Tolong mulai ulang generating session lagi', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('Nomor Telepon masih salah , Tolong mulai ulang generating lagi', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "Tolong cek untuk kode OTP dalam akun Telegram , Jika anda mendapatkannya , Kirim kode OTP disini sesudah membaca format di bawah ini\nJika kode OTP adalah `12345` , **Dan kirim dengan** `1 2 3 4 5` pakai spasi", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('Batas waktu tercapai 10 menit , Tolong mulai ulang generating session lagi', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('Kode OTP ini salah , Tolong mulai ulang generating session lagi', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('Kode OTP ini kadaluarsa , Tolong mulai ulang generating session lagi', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'Akun Anda telah mengaktifkan verifikasi dua langkah , Tolong berikan kata sandinya', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('Batas waktu tercapai 5 menit , Tolong mulai ulang generating session lagi', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('Kata sandi salah , Tolong mulai ulang generating session lagi', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} STRING SESSION** \n\n`{}` \n\nGenerating String Session Bot\n**Support :** @UserbotTelegramSupport".format("TELETHON" if telethon else "PYROGRAM", string_session)
    await client.send_message("me", text)
    await client.disconnect()
    await phone_code_msg.reply("Berhasil Megambil {} string session\n\nSilahkan cek di Pesan Tersimpan\n\nJika ada masalah laporkan ke @tzypis".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Membatalkan Proses!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("Memulai Ulang Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Membatalkan generation proses!", quote=True)
        return True
    else:
        return False


# @Client.on_message(filters.private & ~filters.forwarded & filters.command(['cancel', 'restart']))
# async def formalities(_, msg):
#     if "/cancel" in msg.text:
#         await msg.reply("Membatalkan Semua Proses!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     elif "/restart" in msg.text:
#         await msg.reply("Memulai Ulang Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     else:
#         return False
