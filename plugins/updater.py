import os
import sys
from functools import wraps
import heroku3

from git import Repo
from pyrogram.types import Message
from modules.helpers.command import commandpro
from modules.helpers.filters import command
from pyrogram import Client, filters
from os import system, execle, environ
from modules.helpers.decorators import sudo_users_only
from git.exc import InvalidGitRepositoryError
from modules.config import UPSTREAM_REPO, BOT_USERNAME, HEROKU_API_KEY, HEROKU_APP_NAME


def gen_chlog(repo, diff):
    upstream_repo_url = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = tldr_log = ""
    ch = f"<b>updates for <a href={upstream_repo_url}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b>"
            f"<a href={upstream_repo_url.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        )
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head("main", origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)
    ac_br = repo.active_branch.name
    if "upstream" in repo.remotes:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", UPSTREAM_REPO)
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


@Client.on_message(command(["update", f"update@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def update_repo(_, message: Message):
    chat_id = message.chat.id
    msg = await message.reply("🔄 `processing update...`")
    update_avail = updater()
    if update_avail:
        await msg.edit("✅ ᴜᴘᴅᴀᴛᴇ ғɪɴɪsʜᴇᴅ\n✅ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ, ʙᴀᴄᴋ ᴀᴄᴛɪᴠᴇ ᴀɢᴀɪɴ ɪɴ 1 ᴍɪɴᴜᴛᴇ")
        system("git pull -f && pip3 install -r requirements.txt")
        execle(sys.executable, sys.executable, "main.py", environ)
        return
    await msg.edit("ʙᴏᴛ ɪs ᴜᴘ ᴛᴏ ᴅᴀᴛᴇ ᴡɪᴛʜ [Aɓʜɩɱʌŋƴʋ Rʌŋʌwʌt](https://t.me/Itz_Venom_xD)", disable_web_page_preview=True)


@Client.on_message(command(["restart", f"restart@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def restart_bot(_, message: Message):
    msg = await message.reply("`ʀᴇsᴛᴀʀᴛɪɴɢ ʙᴏᴛ...`")
    args = [sys.executable, "main.py"]
    await msg.edit("✅ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ\n✅ ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ ᴀɢᴀɪɴ")
    execle(sys.executable, *args, environ)
    return



# HEROKU LOGS
async def edit_or_send_as_file(
    text: str,
    message: Message,
    client: Client,
    caption: str = "`Result!`",
    file_name: str = "result",
    parse_mode="md",
):
    """Send As File If Len Of Text Exceeds Tg Limit Else Edit Message"""
    if not text:
        await message.edit("`ᴛʜᴇʀᴇ ɪs sᴏᴍᴇᴛʜɪɴɢ ᴏᴛʜᴇʀ ᴛʜᴀɴ ᴛᴇxᴛ.../nᴀʙᴏʀᴛɪɴɢ...`")
        return
    if len(text) <= 1024:
        return await message.edit(text, parse_mode=parse_mode)

    await message.edit("`ᴏᴜᴛᴘᴜᴛ ɪs ᴛᴏᴏ ʟᴀʀɢᴇ.../nsᴇɴᴅɪɴɢ ᴀs ғɪʟᴇ...`")
    file_names = f"{file_name}.text"
    open(file_names, "w").write(text)
    await client.send_document(message.chat.id, file_names, caption=caption)
    await message.delete()
    if os.path.exists(file_names):
        os.remove(file_names)
    return


heroku_client = heroku3.from_key(HEROKU_API_KEY) if HEROKU_API_KEY else None


def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        heroku_app = None
        if not heroku_client:
            await message.reply_text("`ᴘʟᴇᴀsᴇ ᴀᴅᴅ ʜᴇʀᴏᴋᴜ ᴀᴘɪ ᴋᴇʏ ᴛᴏ ᴜsᴇ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ`")
        elif not HEROKU_APP_NAME:
            await edit_or_reply(
                message, "`ᴘʟᴇᴀsᴇ ᴀᴅᴅ ʜᴇʀᴏᴋᴜ ᴀᴘᴘ ɴᴀᴍᴇ ᴛᴏ ᴜsᴇ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ...`"
            )
        if HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(HEROKU_APP_NAME)
            except:
                await message.reply_text(
                    message,
                    "`ʜᴇʀᴏᴋᴜ ᴀᴘɪ ᴋᴇʏ ᴀɴᴅ ᴀᴘᴘ ɴᴀᴍᴇ ᴅᴏᴇsɴ'ᴛ ᴍᴀᴛᴄʜ, ᴘʟᴇᴀsᴇ ʀᴇᴄʜᴇᴄᴋ...`",
                )
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli


@Client.on_message(commandpro(["Logs", "/logs"]))
@sudo_users_only
@_check_heroku
async def logswen(client: Client, message: Message, happ):
    msg = await message.reply_text("`ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ a ᴍᴏᴍᴇɴᴛ...`")
    logs = happ.get_log()
    capt = f"ʜᴇʀᴏᴋᴜ ʟᴏɢs ᴏғ `{HEROKU_APP_NAME}`"
    await edit_or_send_as_file(logs, msg, client, capt, "logs")

