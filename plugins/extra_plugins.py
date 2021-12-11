import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, User
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
from telegraph import upload_file

UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "pdfmalayalam")


#@Client.on_message(filters.command('id'))
@Client.on_message((filters.command(["report"]) | filters.regex("@admins") | filters.regex("@admin")) & filters.group)
async def report(bot, message):
    if message.reply_to_message:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        admins = await bot.get_chat_members(chat_id=chat_id, filter="administrators")
        success = False
        report = f"Reporter : {mention} ({reporter})" + "\n"
        report += f"Message : {message.reply_to_message.link}"
        for admin in admins:
            try:
                reported_post = await message.reply_to_message.forward(admin.user.id)
                await reported_post.reply_text(
                    text=report,
                    chat_id=admin.user.id,
                    disable_web_page_preview=True
                )
                success = True
            except:
                pass
        if success:
            await message.reply_text("**Reported to Admins!**")


@Client.on_message(filters.command(["banuser"]))
async def ban(bot, message):
    chatid = message.chat.id
    if message.reply_to_message:
        admins_list = await bot.get_chat_members(
            chat_id=chatid, filter="administrators"
        )
        admins = []
        for admin in admins_list:
            id = admin.user.id
            admins.append(id)
        userid = message.from_user.id
        if userid in admins:
            user_to_ban = message.reply_to_message.from_user.id
            if user_to_ban in admins:
                await message.reply(text="Think he is Admin, Can't Ban Admins")
            else:
                try:
                    await bot.kick_chat_member(chat_id=chatid, user_id=user_to_ban)
                    await message.reply_text(
                        f"Bye {message.reply_to_message.from_user.mention}"
                    )
                except Exception as error:
                    await message.reply_text(f"{error}")
        else:
            await message.reply_text("Nice try, But wrong move..")
            return
    else:
        return


@Client.on_message(filters.command(["unbanuser"]))
async def ban(bot, message):
    chatid = message.chat.id
    if message.reply_to_message:
        admins_list = await bot.get_chat_members(
            chat_id=chatid, 
            filter="administrators"
        )
        admins = []
        for admin in admins_list:
            id = admin.user.id
            admins.append(id)
        userid = message.from_user.id
        if userid in admins:
            user_to_ban = message.reply_to_message.from_user.id
            if user_to_unban in admins:
                await message.reply(text="Think he is Admin, Can't Ban Admins")
            else:
                try:
                    await bot.unban_chat_member(chat_id=chatid, user_id=user_to_unban)
                    await message.reply_text(
                        f"welcome {message.reply_to_message.from_user.mention}"
                    )
                except Exception as error:
                    await message.reply_text(f"{error}")
        else:
            await message.reply_text("Nice try, But wrong move..")
            return
    else:
        return
