import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("play") 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
async def play(_, message: Message):

    lel = await message.reply("🔄 **Rᴜᴋᴊᴀ Bᴄ Kʀ Rʜᴀ Hᴜ Sᴀʙᴀʀ Kʀ 🎶🤟**")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "EsportRobot"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>Aᴅ Mᴇ As A Aᴅᴍɪɴ Oғ Yᴏᴜʀ Gʀᴏᴜᴘ Fɪʀsᴛ </b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**Aᴀ Gʏᴀ Mᴇɪɴ Sᴀʙ Nᴀᴄʜᴏ Aʙ Mᴇɪɴ Gᴀɴᴀ Bᴀᴊᴀᴜɴɢᴀ**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>Fʟᴏᴏᴅ Wᴀɪᴛ Eʀʀᴏʀ</b>\Gᴀʏ Assɪsᴛᴀɴᴛ Usᴇʀʙᴏᴛ Cᴏᴜʟᴅ ɴᴏᴛ ᴊᴏɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴅᴜᴇ ᴛᴏ ʜᴇᴀᴠʏ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴍᴀᴋᴇ sᴜʀᴇ ᴜsᴇʀʙᴏᴛ ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>Assɪsᴛᴀɴᴛ ᴜsᴇʀʙᴏᴛ ɪs ɴᴏᴛ ɪɴ ᴛʜɪs ᴄʜᴀᴛ ᴀsᴋ ᴛᴏ sᴇɴᴅ /play ᴄᴏᴍᴍᴍᴀɴᴅ ғᴏʀ ᴀᴅᴅ ᴛʜᴇ ғɪʀsᴛ ᴛɪᴍᴇ</i>")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"Vɪᴅᴇᴏ Lᴀᴍʙɪ Hᴀɪ {DURATION_LIMIT} Yᴇʜ Nᴀ Cʜᴀʟᴇɢɪ Bᴄ ❤️🤞"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/667ed65a936a707c0d19a.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                            text="𝐂ʜᴀɴɴᴇʟ📡",
                            url=f"https://t.me/UNIVERSAL_OP_CHAT"),
                        InlineKeyboardButton(
                            text="𝐆ʀᴏᴜᴘ⭐",
                            url=f"https://t.me/UNIVERSAL_OP_CHAT")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝐂ʜᴀɴɴᴇʟ📡",
                            url=f"https://t.me/UNIVERSAL_OP_CHAT"),
                        InlineKeyboardButton(
                            text="𝐆ʀᴏᴜᴘ⭐",
                            url=f"https://t.me/UNIVERSAL_OP_CHAT")

                    ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/667ed65a936a707c0d19a.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                            text="𝐂ʜᴀɴɴᴇʟ📡",
                            url=f"https://t.me/UNIVERSAL_OP_CHAT"),
                        InlineKeyboardButton(
                            text="𝐆ʀᴏᴜᴘ⭐",
                            url=f"https://t.me/UNIVERSAL_OP_CHAT")

                        ]
                    ]
                )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"Vɪᴅᴇᴏ Lᴀᴍʙʜɪ Hᴀɪ {DURATION_LIMIT} ʏᴇʜ Nᴀ Cʜᴀʟᴇɢɪ Bᴄ ❤️🤞")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("✌**Bᴀᴛᴀ Kᴏɴsᴀ Gᴀɴᴀ Cʜᴀᴀᴛᴀ Hᴀɪ Sᴜɴ Nᴇ K Lɪʏᴇ**")
        await lel.edit("🔎 **Dʜᴜɴᴅ Rʜᴀ Hᴜ Bᴄ**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🎵 **Kʀ Rʜᴀ Hᴜ Rᴜᴋᴊᴀ Bᴄ 🔊**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "🌸Gᴀɴᴀ Nᴀ Mɪʟᴀ Sᴘᴇᴇʟɪɴɢ sʜɪ ᴋʀ."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                      
                        InlineKeyboardButton(
                            text="𝐂ʜᴀɴɴᴇʟ📡",
                            url=f"https://t.me/UNIVERSAL_OP_CHAT"),
                        InlineKeyboardButton(
                            text="𝐆ʀᴏᴜᴘ⭐",
                            url=f"https://t.me/UNIVERSAL_OP_CHAT")
                    ]
                ]
            )
        
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"Vɪᴅᴇᴏ Lᴀᴍʙʜɪ Hᴀɪ {DURATION_LIMIT} Yᴇʜ Nᴀ Cʜᴀʟᴇɢɪ ❤️🤞")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption="**Sᴏɴɢ Pᴏsɪᴛɪᴏɴ 💫🤟** {}".format(
        position
        ),
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="** TᴄDᴏᴘᴀ Mᴜsɪᴄ Bᴏᴛ Now 😄 Pʟᴀʏɪɴɢ 📀 Aᴛ 🤟 `{}`...**".format(
        message.chat.title
        ), )
        os.remove("final.png")
        return await lel.delete()
