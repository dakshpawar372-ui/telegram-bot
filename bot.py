from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import *

# ---------------- CHECK FORCE JOIN ----------------
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
            [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1_LINK)],
            [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2_LINK)],
            [InlineKeyboardButton("✅ Verify", callback_data="verify")]
        ]

        await update.message.reply_text(
            "⚠️ Please join both channels first:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await send_menu(update, context)


# ---------------- MENU ----------------
async def send_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("🔥 INDIAN", callback_data="indian")],
        [InlineKeyboardButton("⚡ VIRAL", callback_data="viral")],
        [InlineKeyboardButton("🇷🇺 RUSSIA", callback_data="russia")],
        [InlineKeyboardButton("🆘 SUPPORT", url=f"https://t.me/{SUPPORT_USERNAME}")]
    ]

    text = "🎬 Welcome! Choose a category:"

    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ---------------- SEND VIDEOS ----------------
async def send_videos(chat_id, category, context):
    if category == "indian":
        data = INDIAN
    elif category == "viral":
        data = VIRAL
    else:
        data = RUSSIA

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
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if not await check_joined(user_id, context):
        await query.message.reply_text("⚠️ Please join channels first.")
        return

    if data == "verify":
        await query.message.reply_text("✅ Verified! Now choose a category.")
        await send_menu(query, context)

    elif data == "indian":
        await query.message.reply_text("🔥 Sending INDIAN videos...")
        await send_videos(query.message.chat_id, "indian", context)

    elif data == "viral":
        await query.message.reply_text("⚡ Sending VIRAL videos...")
        await send_videos(query.message.chat_id, "viral", context)

    elif data == "russia":
        await query.message.reply_text("🇷🇺 Sending RUSSIA videos...")
        await send_videos(query.message.chat_id, "russia", context)


# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()