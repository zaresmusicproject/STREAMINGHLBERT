import asyncio
import random

from pyrogram import Client, filters

APAKAH_TEXT = [
    "Iya",
    "Tidak",
    "Bukan",
    "Mungkin",
    "Betul",
    "Benar",
    "Mungkin tidak",
    "Mungkin iya",
    "Beneran",
    "Iyakah",
    "Apa",
    "Nggak tau",
    "Tidak tahu",
    "Entah",
    "Entahlah",
    "Nggak gitu",
    "0hya",
    "Masuk akal",
    "Pasti",
    "Tentu saja",
    "Sudah",
    "Sudah pasti",
    "Apa iya",
    "Betulkah",
    "Ah masa",
    "Begitu",
    "Begitu ya",
    "Kayaknya",
    "Kayaknya sih",
    "Kayaknya iya",
    "Kayaknya gitu",
    "Masashi",
    "Oh gitu",
    "Oh okay",
    "Mustahil",
    "Tidak mungkin",
    "Tidak usah",
    "Tidak perlu",
    "Perlukah",
    "Mungkin saja",
]

# Buat Senang-senang saja
@Client.on_message(filters.regex("apakah|Apakah|APAKAH"))
async def apakah(tomi, message):
    await tomi.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(2)
    await message.reply(random.choice(APAKAH_TEXT))
