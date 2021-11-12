from asyncio.queues import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message
from callsmusic import callsmusic

from config import BOT_NAME as BN
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'
    ):
        await message.reply_text("❗ Kᴜᴄʜ Cʜᴀʟ Hɪ Nʜɪ Rʜᴀ ✨")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("▶️ Cʜᴜᴘ Hᴏ Gʏᴀ Bᴄ 😔")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'
    ):
        await message.reply_text("❗ Kᴜᴄʜ Cʜᴀʟ Hɪ Nʜɪ Rʜᴀ ✨")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("⏸ Cʜᴀʟᴏ Hᴏ Gʏᴀ Bᴄ 🤩")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ Kᴜᴄʜ Cʜᴀʟ Hɪ Nʜɪ Rʜᴀ ✨")
    else:
        try:
            callsmusic.queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text("❌ Rᴜᴋɢʏᴀ Bsᴅᴋ Bss ✨")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗Kᴜᴄʜ Cʜᴀʟᴜ Hɪ Nʜɪ Hᴀɪ Tᴏ Kʏᴀ Gʜᴀɴᴛᴀ Sᴋɪᴘ Kʀᴜ 🥀")
    else:
        callsmusic.queues.task_done(message.chat.id)

        if callsmusic.queues.is_empty(message.chat.id):
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                message.chat.id,
                callsmusic.queues.get(message.chat.id)["file"]
            )

        await message.reply_text("➡️ Gᴀɴᴀ Sᴋɪᴘ Kʀ Dɪᴀ Pᴀʀᴛʏ 🥀")
