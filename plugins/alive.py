import asyncio
from time import time
from datetime import datetime
from modules.config import BOT_USERNAME
from modules.helpers.filters import command
from modules.helpers.command import commandpro
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)
    
   

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/de138de8fd880becb9cf1.jpg",
        caption=f"""**━━━━━━━━━━━━━━━━━━━━━━━━
💥 𝐇𝐨𝐢, 𝐈 𝐚𝐦 𝐀𝐥𝐢𝐬𝐡𝐚 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐒𝐮𝐩𝐞𝐫𝐟𝐚𝐬𝐭
   𝐕𝐜 𝐌𝐮𝐬𝐢𝐜 𝐩𝐥𝐚𝐲𝐞𝐫 𝐟𝐨𝐫 𝐘𝐨𝐮𝐫 𝐥𝐨𝐯𝐞𝐥𝐲 𝐆𝐫𝐨𝐮𝐩...
┏━━━━━━━━━━━━━━━━━┓
┣★ ᴄʀᴇᴀᴛᴏʀ : [𝐂𝐚𝐧𝐝𝐲 𝐐𝐮𝐞𝐞𝐧](https://t.me/candy_626)
┣★ ᴜᴘᴅᴀᴛᴇs : [𝐂𝐡𝐚𝐧𝐧𝐞𝐥](https://t.me/Pubglovers_shayri_lovers)
┣★ sᴜᴘᴘᴏʀᴛ : [𝐆𝐫𝐨𝐮𝐩](https://t.me/AlishaSupport)
┣★ ᴏᴡɴᴇʀ   : [𝐕𝐞𝐧𝐨𝐦](https://t.me/Itz_Venom_xD)
┗━━━━━━━━━━━━━━━━━┛

💞 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ
ᴅᴍ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](https://t.me/Itz_Venom_xD) ...
━━━━━━━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ❰ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ❱ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
                
           ]
        ),
    )
    
    
@Client.on_message(commandpro(["Candy", "/start", "/alive", "@Itz_VeNom_xD"]) & filters.private & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/de138de8fd880becb9cf1.jpg",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💥 ᴊᴏɪɴ ʜᴇʀᴇ ᴀɴᴅ sᴜᴘᴘᴏʀᴛ 💞", url=f"https://t.me/AlishaSupport")
                ]
            ]
        ),
    )


@Client.on_message(commandpro(["repo", "/repo"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/de138de8fd880becb9cf1.jpg",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💥 ᴄʟɪᴄᴋ ᴍᴇ ᴛᴏ ɢᴇᴛ ʀᴇᴘᴏ 💞", url=f"https://github.com/AbhumanyuXMusic/HeroMusic")
                ]
            ]
        ),
    )
