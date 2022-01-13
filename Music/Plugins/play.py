import asyncio
import os
import random
import shutil
from os import path

import yt_dlp
from Music import ASSID, ASSNAME, ASSUSERNAME, BOT_ID, BOT_NAME, app
from Music.config import DURATION_LIMIT
from Music.MusicUtilities.database.chats import add_served_chat, is_served_chat
from Music.MusicUtilities.database.onoff import is_on_off
from Music.MusicUtilities.database.queue import (
    add_active_chat,
    is_active_chat,
    music_on,
    remove_active_chat,
)
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.fsubs import subcribe
from Music.MusicUtilities.helpers.gets import get_url, themes
from Music.MusicUtilities.helpers.inline import (
    audio_markup,
    play_markup,
    playlist_markup,
    search_markup,
    search_markup2,
)
from Music.MusicUtilities.helpers.logger import LOG_CHAT
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.MusicUtilities.tgcallsrun import ASS_ACC, convert, download, music, put
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, Message, Voice
from pytgcalls import StreamType
from Music.MusicUtilities.helpers.decorators import authorized_users_only
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from youtubesearchpython import VideosSearch

flex = {}
chat_watcher_group = 3


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
que = {}

@app.on_message(
    command("music") & ~filters.group
)
@authorized_users_only
async def music_onoff(_, message: Message):
    global DISABLED_GROUPS
    try:
        message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text("**• usage:**\n\n `/music on` & `/music off`")
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status in ("ON", "on", "On"):
        lel = await message.reply("`tunggu sebentar...`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **Music Telah Aktif ✅**")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"**✅ Music Telah Di Diaktifkan Di {message.chat.title}**"
        )

    elif status in ("OFF", "off", "Off"):
        lel = await message.reply("`processing...`")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **Music Tidak Aktif❌.**")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"**✅ Music Telah Di Nonaktifkan Di {message.chat.title} !**"
        )
    else:
        await message.reply_text(
            "**• Penggunaan:**\n\n `/music on` & `/music off`"
        )


@Client.on_message(command(["play", "play@Tg_Vc_00_Bot"]))
@subcribe
async def play(_, message: Message):
    chat_id = message.chat.id
    global que
    global useer
    if chat_id in DISABLED_GROUPS:
        return await message.reply_text(
            f"😕 **Maaf kak {message.from_user.mention}, Musicnya sedang tidak aktif,tag Admin untuk mengaktifkan**" 
        )
    if not await is_served_chat(chat_id):
        await add_served_chat(chat_id)
    if message.sender_chat:
        return await message.reply_text(
            "You're an __Anonymous Admin__!\nRevert back to User Account From Admin Rights."
        )
    user_id = message.from_user.id
    chat_title = message.chat.title
    message.from_user.first_name
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_on_off(1):
        LOG_ID = "-1001429892362"
        if int(chat_id) != int(LOG_ID):
            return await message.reply_text(
                f"Bot is under Maintenance. Sorry for the inconvenience!"
            )
        return await message.reply_text(
            f"Bot is under Maintenance. Sorry for the inconvenience!"
        )
    a = await app.get_chat_member(message.chat.id, BOT_ID)
    if a.status != "administrator":
        await message.reply_text(
            f"I need to be admin with some permissions:\n\n- **can_manage_voice_chats:** To manage voice chats\n- **can_delete_messages:** To delete Music's Searched Waste\n- **can_invite_users**: For inviting assistant to chat\n**can_restrict_members**: For Protecting Music from Spammers."
        )
        return
    if not a.can_manage_voice_chats:
        await message.reply_text(
            "I don't have the required permission to perform this action."
            + "\n**Permission:** __MANAGE VOICE CHATS__"
        )
        return
    if not a.can_delete_messages:
        await message.reply_text(
            "I don't have the required permission to perform this action."
            + "\n**Permission:** __DELETE MESSAGES__"
        )
        return
    if not a.can_invite_users:
        await message.reply_text(
            "I don't have the required permission to perform this action."
            + "\n**Permission:** __INVITE USERS VIA LINK__"
        )
        return
    if not a.can_restrict_members:
        await message.reply_text(
            "I don't have the required permission to perform this action."
            + "\n**Permission:** __BAN USERS__"
        )
        return
    try:
        b = await app.get_chat_member(message.chat.id, ASSID)
        if b.status == "kicked":
            await message.reply_text(
                f"{ASSNAME}(@{ASSUSERNAME}) is banned in your chat **{chat_title}**\n\nUnban it first to use Music"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ASS_ACC.join_chat(f"{message.chat.username}")
                await message.reply(
                    f"{ASSNAME} Joined Successfully",
                )
                await remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_text(
                    f"__**Assistant Failed To Join**__\n\n**Reason**:{e}"
                )
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
                    await ASS_ACC.join_chat(f"https://t.me/joinchat/{link_hash}")
                return await message.reply(
                    f"{ASSNAME} Successfully Joined Groups",
                )
                await remove_active_chat(chat_id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(
                    f"__**Assistant Failed to Join Groups**__\n\n**Reason**:{e}"
                )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    await message.delete()
    fucksemx = 0
    if audio:
        fucksemx = 1
        what = "Audio Searched"
        await LOG_CHAT(message, what)
        mystic = await message.reply_text(f"**💸 Processing Your Song....**")
        if audio.file_size > 157286400:
            await mystic.edit_text("Audio File Size Should Be Less Than 150 mb")
            return
        duration = round(audio.duration / 60)
        if duration > DURATION_LIMIT:
            return await mystic.edit_text(
                f"**__Duration Error__**\n\n**Allowed Duration: **{DURATION_LIMIT} minute(s)\n**Received Duration:** {duration} minute(s)"
            )
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file_name = path.join(path.realpath("downloads"), file_name)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(file_name))
            else file_name,
        )
        title = "Selected Audio from Telegram"
        link = "https://t.me/unclesamaja1"
        thumb = "cache/photo_2022-01-08_21-56-13.jpg"
        videoid = "smex1"
    elif url:
        what = "URL Searched"
        await LOG_CHAT(message, what)
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("Processing Url")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"]
                link = result["link"]
                (result["id"])
                videoid = result["id"]
        except Exception as e:
            return await mystic.edit_text(f"Soung Not Found.\n**Possible Reason:**{e}")
        smex = int(time_to_seconds(duration))
        if smex > DURATION_LIMIT:
            return await mystic.edit_text(
                f"**__Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)"
            )
        if duration == "None":
            return await mystic.edit_text("Sorry! Live videos are not Supported")
        if views == "None":
            return await mystic.edit_text("Sorry! Live videos are not Supported")
        semxbabes = f"Downloading {title[:50]}"
        await mystic.edit(semxbabes)
        theme = random.choice(themes)
        ctitle = message.chat.title
        ctitle = await CHAT_TITLE(ctitle)
        userid = message.from_user.id
        thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                    except Exception:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                mystic.edit(
                    f"**❤️‍🔥 Downloaded {title[:50]}.....**\n\n**📚 FileSize:** {size}\n**⚡ Time Taken:** {taken} sec\n\n**📑 Converting Music File**"
                )
                print(f"[{videoid}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, link, my_hook)
        file = await convert(x)
    else:
        if len(message.command) < 2:
            what = "Command"
            await LOG_CHAT(message, what)
            user_name = message.from_user.first_name
            thumb = "cache/photo_2022-01-08_21-56-13.jpg"
            buttons = playlist_markup(user_name, user_id)
            hmo = await message.reply_photo(
                photo=thumb,
                caption=(
                    "**Usage:** /play [Music Name Or Youtube Link Or Reply to Audio]\n\nIf You Want To Play Playlists! Select The One From Below.\n\n**More Info In [Group](t.me/unclesamaja1)**"
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        what = "Query Given"
        await LOG_CHAT(message, what)
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("**🔎 Searching Song**")
        try:
            a = VideosSearch(query, limit=5)
            result = (a.result()).get("result")
            title1 = result[0]["title"]
            duration1 = result[0]["duration"]
            title2 = result[1]["title"]
            duration2 = result[1]["duration"]
            title3 = result[2]["title"]
            duration3 = result[2]["duration"]
            title4 = result[3]["title"]
            duration4 = result[3]["duration"]
            title5 = result[4]["title"]
            duration5 = result[4]["duration"]
            ID1 = result[0]["id"]
            ID2 = result[1]["id"]
            ID3 = result[2]["id"]
            ID4 = result[3]["id"]
            ID5 = result[4]["id"]
        except Exception as e:
            return await mystic.edit_text(f"Song Not Found.\n**Possible Reason:**{e}")
        thumb = "cache/IMG_2.png"
        await mystic.delete()
        buttons = search_markup(
            ID1,
            ID2,
            ID3,
            ID4,
            ID5,
            duration1,
            duration2,
            duration3,
            duration4,
            duration5,
            user_id,
            query,
        )
        hmo = await message.reply_photo(
            photo=thumb,
            caption=(
                f"1️⃣<b>{title1[:25]}</b>\n┣ ❤️‍🔥 __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID1})__</u>\n\n2️⃣<b>{title2[:25]}</b>\n┣ ❤️‍🔥 __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID2})__</u>\n\n3️⃣<b>{title3[:25]}</b>\n┣ ❤️‍🔥 __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID3})__</u>\n\n4️⃣<b>{title4[:25]}</b>\n┣ ❤️‍🔥 __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID4})__</u>\n\n5️⃣<b>{title5[:25]}</b>\n┣ ❤️‍🔥 __Powered {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID5})__</u>"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return
    if await is_active_chat(chat_id):
        position = await put(chat_id, file=file)
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        cpl = f"downloads/{_chat_}final.png"
        shutil.copyfile(thumb, cpl)
        f20 = open(f"search/{_chat_}title.txt", "w")
        f20.write(f"{title}")
        f20.close()
        f111 = open(f"search/{_chat_}duration.txt", "w")
        f111.write(f"{duration}")
        f111.close()
        f27 = open(f"search/{_chat_}username.txt", "w")
        f27.write(f"{checking}")
        f27.close()
        if fucksemx != 1:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = play_markup(videoid, user_id)
        else:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = audio_markup(videoid, user_id)
        checking = (
            f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )
        await message.reply_photo(
            photo=thumb,
            caption=(
                f"💡 **Track Added To Queue »** `{position}`\n\n🏷️<b> **Title:** </b>[{title[:25]}]({url}) \n⏳🕰️<b> **Duration:** </b> {duration} \n🎧<b> **Requested By:** </b>{checking}"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return await mystic.delete()
    else:
        await music_on(chat_id)
        await add_active_chat(chat_id)
        await music.pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    file,
                ),
            ),
            stream_type=StreamType().local_stream,
        )
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        checking = (
            f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )
        if fucksemx != 1:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = play_markup(videoid, user_id)
        else:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = audio_markup(videoid, user_id)
        await message.reply_photo(
            photo=thumb,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=(
                f"🏷️<b> **Title:** </b>[{title[:25]}]({url}) \n🕰️<b> **Duration:** </b> {duration} \n🎧<b> **Requested by:** </b>{checking}"
            ),
        )
        return await mystic.delete()


@Client.on_callback_query(filters.regex(pattern=r"Music"))
async def startyuplay(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    CallbackQuery.message.chat.title
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    try:
        id, duration, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"Error Occured\n**Possible reason could be**:{e}"
        )
    if duration == "None":
        return await CallbackQuery.message.reply_text(
            f"Sorry!, Live Videos are not supported"
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "This is not for you! Search You Own Song nigga", show_alert=True
        )
    await CallbackQuery.message.delete()
    checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    url = f"https://www.youtube.com/watch?v={id}"
    videoid = id
    smex = int(time_to_seconds(duration))
    if smex > DURATION_LIMIT:
        await CallbackQuery.message.reply_text(
            f"**__Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)"
        )
        return
    try:
        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
            x = ytdl.extract_info(url, download=False)
    except Exception as e:
        return await CallbackQuery.message.reply_text(
            f"Failed to download this video.\n\n**Reason**:{e}"
        )
    title = x["title"]
    await CallbackQuery.answer(
        f"Selected {title[:20]}.... \nProcessing..", show_alert=True
    )
    mystic = await CallbackQuery.message.reply_text(f"Downloading {title[:50]}")
    thumbnail = x["thumbnail"]
    (x["id"])
    videoid = x["id"]

    def my_hook(d):
        if d["status"] == "downloading":
            percentage = d["_percent_str"]
            per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
            per = int(per)
            eta = d["eta"]
            speed = d["_speed_str"]
            size = d["_total_bytes_str"]
            bytesx = d["total_bytes"]
            if str(bytesx) in flex:
                pass
            else:
                flex[str(bytesx)] = 1
            if flex[str(bytesx)] == 1:
                flex[str(bytesx)] += 1
                try:
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                except Exception:
                    pass
            if per > 250:
                if flex[str(bytesx)] == 2:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
            if per > 500:
                if flex[str(bytesx)] == 3:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
            if per > 800:
                if flex[str(bytesx)] == 4:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
        if d["status"] == "finished":
            try:
                taken = d["_elapsed_str"]
            except Exception:
                taken = "00:00"
            size = d["_total_bytes_str"]
            mystic.edit(
                f"**📥 Downloaded {title[:50]}.....**\n\n**📚 FileSize:** {size}\n**⌛ Time Taken:** {taken} sec\n\n**📑 Converting Flicks File**"
            )
            print(f"[{videoid}] Downloaded| Elapsed: {taken} seconds")

    loop = asyncio.get_event_loop()
    x = await loop.run_in_executor(None, download, url, my_hook)
    file = await convert(x)
    theme = random.choice(themes)
    ctitle = CallbackQuery.message.chat.title
    ctitle = await CHAT_TITLE(ctitle)
    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
    await mystic.delete()
    if await is_active_chat(chat_id):
        position = await put(chat_id, file=file)
        buttons = play_markup(videoid, user_id)
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        cpl = f"downloads/{_chat_}final.png"
        shutil.copyfile(thumb, cpl)
        f20 = open(f"search/{_chat_}title.txt", "w")
        f20.write(f"{title}")
        f20.close()
        f111 = open(f"search/{_chat_}duration.txt", "w")
        f111.write(f"{duration}")
        f111.close()
        f27 = open(f"search/{_chat_}username.txt", "w")
        f27.write(f"{checking}")
        f27.close()
        f28 = open(f"search/{_chat_}videoid.txt", "w")
        f28.write(f"{videoid}")
        f28.close()
        await mystic.delete()
        m = await CallbackQuery.message.reply_photo(
            photo=thumb,
            caption=(
                f"💡 **Track added to queue »** `{position}`\n\n🏷️<b> **Title:** </b>[{title[:25]}]({url}) \n🕰️<b> **Duration:** </b> {duration} \n🎧<b> **Requested by:** </b>{checking}"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        os.remove(thumb)
        await CallbackQuery.message.delete()
    else:
        await music_on(chat_id)
        await add_active_chat(chat_id)
        await music.pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    file,
                ),
            ),
            stream_type=StreamType().local_stream,
        )
        buttons = play_markup(videoid, user_id)
        await mystic.delete()
        m = await CallbackQuery.message.reply_photo(
            photo=thumb,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=(
                f"🏷️<b> **Title:** </b>[{title[:25]}]({url}) \n🕰️<b> **Duration:** </b> {duration} \n🎧<b> **Requested by:** </b>{checking}"
            ),
        )
        os.remove(thumb)
        await CallbackQuery.message.delete()


@Client.on_callback_query(filters.regex(pattern=r"popat"))
async def popat(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    print(callback_request)
    CallbackQuery.from_user.id
    try:
        id, query, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"Error Occured\n**Possible reason could be**:{e}"
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "This is not for you! Search You Own Song", show_alert=True
        )
    i = int(id)
    query = str(query)
    try:
        a = VideosSearch(query, limit=10)
        result = (a.result()).get("result")
        title1 = result[0]["title"]
        duration1 = result[0]["duration"]
        title2 = result[1]["title"]
        duration2 = result[1]["duration"]
        title3 = result[2]["title"]
        duration3 = result[2]["duration"]
        title4 = result[3]["title"]
        duration4 = result[3]["duration"]
        title5 = result[4]["title"]
        duration5 = result[4]["duration"]
        title6 = result[5]["title"]
        duration6 = result[5]["duration"]
        title7 = result[6]["title"]
        duration7 = result[6]["duration"]
        title8 = result[7]["title"]
        duration8 = result[7]["duration"]
        title9 = result[8]["title"]
        duration9 = result[8]["duration"]
        title10 = result[9]["title"]
        duration10 = result[9]["duration"]
        ID1 = result[0]["id"]
        ID2 = result[1]["id"]
        ID3 = result[2]["id"]
        ID4 = result[3]["id"]
        ID5 = result[4]["id"]
        ID6 = result[5]["id"]
        ID7 = result[6]["id"]
        ID8 = result[7]["id"]
        ID9 = result[8]["id"]
        ID10 = result[9]["id"]
    except Exception as e:
        return await mystic.edit_text(f"Soung Not Found.\n**Possible Reason:**{e}")
    if i == 1:
        buttons = search_markup2(
            ID6,
            ID7,
            ID8,
            ID9,
            ID10,
            duration6,
            duration7,
            duration8,
            duration9,
            duration10,
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"6️⃣<b>{title6[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID6})__</u>\n\n7️⃣<b>{title7[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID7})__</u>\n\n8️⃣<b>{title8[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID8})__</u>\n\n9️⃣<b>{title9[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID9})__</u>\n\n🔟<b>{title10[:25]}</b>\n┣ ⚡ Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID10})__</u>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return
    if i == 2:
        buttons = search_markup(
            ID1,
            ID2,
            ID3,
            ID4,
            ID5,
            duration1,
            duration2,
            duration3,
            duration4,
            duration5,
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"1️⃣<b>{title1[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID1})__</u>\n\n2️⃣<b>{title2[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID2})__</u>\n\n3️⃣<b>{title3[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID3})__</u>\n\n4️⃣<b>{title4[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID4})__</u>\n\n5️⃣<b>{title5[:25]}</b>\n┣ ⚡ __Powered By {BOT_NAME}__\n┗ 💎 <u>__[𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13 start=info_{ID5})__</u>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return


@app.on_message(filters.command("playplaylist"))
async def play_playlist_cmd(_, message):
    thumb = "cache/photo_2022-01-08_21-56-13.jpg"
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    buttons = playlist_markup(user_name, user_id)
    await message.reply_photo(
        photo=thumb,
        caption=(
            "**__Music's Playlist Feature__**\n\nSelect the Playlist you want to play!."
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return
