from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import *

# ---------------- FORCE JOIN CHECK ----------------
async def check_joined(user_id, context):
    try:
        m1 = await context.bot.get_chat_member(CHANNEL_1, user_id)
        m2 = await context.bot.get_chat_member(CHANNEL_2, user_id)

        if m1.status in ["left", "kicked"] or m2.status in ["left", "kicked"]:
            return False
        return True
    except:
        return False


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await check_joined(user_id, context):
        keyboard = [
            [InlineKeyboardButton("Join 1", url=CHANNEL_1_LINK)],
            [InlineKeyboardButton("Join 2", url=CHANNEL_2_LINK)],
            [InlineKeyboardButton("Verify", callback_data="verify")]
        ]

        await update.message.reply_text(
            "Join channels first",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await menu(update, context)


# ---------------- MENU ----------------
async def menu(update, context):
    keyboard = [
        [InlineKeyboardButton("INDIAN", callback_data="indian")],
        [InlineKeyboardButton("VIRAL", callback_data="viral")],
        [InlineKeyboardButton("RUSSIA", callback_data="russia")],
        [InlineKeyboardButton("SUPPORT", url=f"https://t.me/{SUPPORT_USERNAME}")]
    ]

    text = "Choose category"

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ---------------- VIDEOS ----------------
async def send_videos(chat_id, category, context):
    data = INDIAN if category == "indian" else VIRAL if category == "viral" else RUSSIA

    for msg_id in data:
        try:
            await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=STORAGE_CHANNEL,
                message_id=msg_id
            )
        except:
            pass


# ---------------- CALLBACK ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "verify":
        await query.message.reply_text("Verified")
        await menu(query, context)

    elif data in ["indian", "viral", "russia"]:
        await query.message.reply_text("Sending videos...")
        await send_videos(query.message.chat_id, data, context)


# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()