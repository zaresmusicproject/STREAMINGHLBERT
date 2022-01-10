import yt_dlp
from Music import (
    ASSID,
    BOT_ID,
    BOT_NAME,
    BOT_USERNAME,
    OWNER,
    SUDOERS,
    app,
)
from Music.MusicUtilities.database.chats import is_served_chat
from Music.MusicUtilities.database.queue import remove_active_chat
from Music.MusicUtilities.database.sudo import get_sudoers
from Music.MusicUtilities.helpers.inline import personal_markup
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.config import GROUP, CHANNEL
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ​", url=f"https://t.me/unclesamaja1"),
            InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/unclesamaja"),
        ],
        [
            InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅ​", url="https://t.me/unclesamaja/40"),
        ],
    ]
    return (
        "🎛 **{BOT_NAME} Merupakan salah satu dari bot telegram yang bisa memutar musik di grup**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
            InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url=f"https://t.me/unclesamaja1"),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/unclesamaja"),
        ],
        [
            InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅ ᴍᴜꜱɪᴄ", url="https://t.me/unclesamaja/40"),
            InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅ ꜱᴛʀᴇᴀᴍ", url="https://t.me/unclesamaja/40"),
        ],
    ]
)
welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(
                    f"🦸🏻‍♂️ **Pemilik Bot [{member.mention}] baru saja bergabung di grup ini.**"
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"**🤖 Admin Bot [{member.mention}] baru saja bergabung di grup ini.**"
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
👋 ** Halo senang rasanya bisa bergabung di grup ini**

💡 **Jangan lupa untuk menjadikan saya sebagai admin di grup ini**
""",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                    disable_web_page_preview=True
                )
                return
        except BaseException:
            return


@Client.on_message(
    filters.group
    & filters.command(
        ["start", "help", f"start@{BOT_USERNAME}", f"help@{BOT_USERNAME}"]
    )
)
async def start(_, message: Message):
    chat_id = message.chat.id
    out = start_pannel()
    await message.reply_text(
        f"""
Terima kasih telah memasukkan saya di {message.chat.title}.
Musik itu hidup.

Untuk bantuan silahkan klik tombol dibawah.
""",
        reply_markup=InlineKeyboardMarkup(out[1]),
        disable_web_page_preview=True
    )
    return


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await app.send_message(
            message.chat.id,
            text=f"""
**✨ Hello {rpk}!  How Are You?
💭 𝐈𝐧𝐢 𝐝𝐢 𝐤𝐞𝐥𝐨𝐥𝐚 𝐨𝐥𝐞𝐡 **[HALBERT](https://t.me/rdwan_13)**, 𝐝𝐚𝐧 𝐛𝐢𝐬𝐚 𝐦𝐞𝐦𝐛𝐚𝐧𝐭𝐮 𝐤𝐚𝐥𝐢𝐚𝐧 𝐮𝐧𝐭𝐮𝐤 𝐦𝐞𝐧𝐝𝐞𝐧𝐠𝐚𝐫 𝐤𝐚𝐧 𝐦𝐮𝐬𝐢𝐜 𝐦𝐞𝐥𝐚𝐥𝐮𝐢 𝐨𝐛𝐫𝐨𝐥𝐚𝐧 𝐬𝐮𝐚𝐫𝐚 𝐆𝐑𝐎𝐔𝐏 𝐭𝐞𝐥𝐞𝐠𝐫𝐚𝐦 (𝐕𝐂𝐆)
            
𝗗𝗮𝗻 𝗦𝗮𝘆𝗮 𝗠𝗲𝗺𝗶𝗹𝗶𝗸𝗶 𝗙𝗶𝘁𝘂𝗿 𝗦𝗲𝗽𝗲𝗿𝘁𝗶 :
• 𝗠𝗲𝗻𝗰𝗮𝗿𝗶 𝗗𝗮𝗻 𝗠𝗲𝗺𝘂𝘁𝗮𝗿 𝗟𝗮𝗴𝘂 𝗬𝗮𝗻𝗴 𝗞𝗮𝗺𝘂 𝗜𝗻𝗴𝗶𝗻𝗸𝗮𝗻.
• 𝗠𝗲𝗺𝘂𝘁𝗮𝗿 𝗩𝗱𝗲𝗼 𝗦𝗲𝗰𝗮𝗿𝗮 𝗕𝗲𝗿𝘀𝗮𝗺𝗮𝗮𝗻 𝗗𝗶 𝗚𝗥𝗢𝗨𝗣 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺,𝗗𝗮𝗻
• 𝗠𝗲𝗻𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗟𝗮𝗴𝘂 𝗬𝗮𝗻𝗴 𝗜𝗻𝗴𝗶𝗻 𝗞𝗮𝗺𝘂 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱.
• 𝗠𝗲𝗻𝗱𝗼𝗻𝗮𝘀𝗶 𝗞𝗮𝗻 𝗞𝗲 𝗢𝘄𝗻𝗲𝗿 𝗕𝗼𝘁 𝗦𝗲 𝗜𝗸𝗵𝗹𝗮𝘀 𝗻𝘆𝗮,𝗝𝗶𝗸𝗮 𝗞𝗮𝗺𝘂 𝗞𝗲𝗹𝗲𝗯𝗶𝗵𝗮𝗻 𝗨𝗮𝗻𝗴.
🌹 𝐒𝐩𝐞𝐜𝐢𝐚𝐥 𝐓𝐡𝐚𝐧𝐤𝐬 𝐓𝐨 : **𝐇𝐀𝐋𝐁𝐄𝐑𝐓** 🌹

👑 𝐎𝐰𝐧𝐞𝐫 : **[𝐇𝐚𝐥𝐛𝐞𝐫𝐭](https://t.me/rdwan_13)**

🤖 [{BOT_NAME}](tg://user?id=2129263636) ᴀᴅᴀʟᴀʜ ʙᴏᴛ ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴅɪɢᴜɴᴀᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴇɴɢᴀʀᴋᴀɴ ʟᴀɢᴜ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ ꜱᴜᴀʀᴀ ᴅᴀɴ ᴅᴀᴘᴀᴛ ᴍᴇᴍᴜᴛᴀʀ ᴠɪᴅᴇᴏ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ ꜱᴜᴀʀᴀ !

📕 ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ꜱᴇᴍᴜᴀ ʙᴏᴛ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴛᴇʀꜱᴇᴅɪᴀ, ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴋᴀɴ ᴅᴜᴀ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ, ʏᴀɪᴛᴜ ᴄᴍᴅ ᴍᴜꜱɪᴄ ᴅᴀɴ ᴄᴍᴅ ꜱᴛʀᴇᴀᴍ**

""",
            parse_mode="markdown",
            reply_markup=pstart_markup,
            reply_to_message_id=message.message_id,
        )
    elif len(message.command) == 2:
        query = message.text.split(None, 1)[1]
        f1 = query[0]
        f2 = query[1]
        f3 = query[2]
        finxx = f"{f1}{f2}{f3}"
        if str(finxx) == "inf":
            query = (str(query)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = x["thumbnail"]
            searched_text = f"""
🔍 **Video Track Information**

❇️**Judul:** {x["title"]}

⏳ **Durasi:** {round(x["duration"] / 60)} Mins
👀 **Ditonton:** `{x["view_count"]}`
👍 **Suka:** `{x["like_count"]}`
👎 **Tidak suka:** `{x["dislike_count"]}`
⭐️ **Peringkat Rata-rata:** {x["average_rating"]}
🎥 **Nama channel:** {x["uploader"]}
📎 **Channel Link:** [Kunjungi Dari Sini]({x["channel_url"]})
🔗 **Link:** [Link]({x["webpage_url"]})
"""
            link = x["webpage_url"]
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(
                message.chat.id,
                photo=thumb,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**💻 DAFTAR PENGGUNA SUDO**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue
                text += f"- {user}\n"
            if not text:
                await message.reply_text("Tidak Ada Pengguna Sudo")
            else:
                await message.reply_text(text)
