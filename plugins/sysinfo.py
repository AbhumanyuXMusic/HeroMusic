import re
import uuid
import socket

import psutil
import platform
from modules.config import BOT_USERNAME
from modules.helpers.command import commandpro
from pyrogram import Client, filters
from modules.helpers.decorators import humanbytes


# FETCH SYSINFO

@Client.on_message(commandpro(["Sysinfo", "/sysinfo", "sysinfo@{BOT_USERNAME}", "Alisha", "Bot", "Admin"]) & ~filters.edited)
async def give_sysinfo(client, message):
    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    ram = humanbytes(round(psutil.virtual_memory().total))
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    du = psutil.disk_usage(client.workdir)
    psutil.disk_io_counters()
    disk = f"{humanbytes(du.used)} / {humanbytes(du.total)} " f"({du.percent}%)"
    cpu_len = len(psutil.Process().cpu_affinity())
    somsg = f"""🤖 **sʏsᴛᴇᴍ ɪɴғᴏʀᴍᴀᴛɪᴏɴ** 🤖
    
**ᴘʟᴀᴛғᴏʀᴍ :** `{splatform}`
**ᴘʟᴀᴛғᴏʀᴍ - ʀᴇʟᴇᴀsᴇ :** `{platform_release}`
**ᴘʟᴀᴛғᴏʀᴍ - ᴠᴇʀsɪᴏɴ :** `{platform_version}`
**ᴀʀᴄʜɪᴛᴇᴄᴛᴜʀᴇ :** `{architecture}`
**ʜᴏsᴛɴᴀᴍᴇ :** `{hostname}`
**ɪᴘ :** `{ip_address}`
**ᴍᴀᴄ :** `{mac_address}`
**ᴘʀᴏᴄᴇssᴏʀ :** `{processor}`
**ʀᴀᴍ : ** `{ram}`
**ᴄᴘᴜ :** `{cpu_len}`
**ᴄᴘᴜ ғʀᴇǫ :** `{cpu_freq}`
**ᴅɪsᴋ :** `{disk}`
    """
    await message.reply(somsg)
