from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import config

# ---------------- CHECK JOIN ----------------
async def check_joined(user_id, context):
    try:
        m1 = await context.bot.get_chat_member(config.CHANNEL_1, user_id)
        m2 = await context.bot.get_chat_member(config.CHANNEL_2, user_id)

        if m1.status in ["left", "kicked"] or m2.status in ["left", "kicked"]:
            return False
        return True
    except:
        return False


# ---------------- MENU ----------------
async def send_menu(chat_id, context):
    keyboard = [
        [InlineKeyboardButton("🔥 INDIAN", callback_data="indian")],
        [InlineKeyboardButton("⚡ VIRAL", callback_data="viral")],
        [InlineKeyboardButton("🇷🇺 RUSSIA", callback_data="russia")],
        [InlineKeyboardButton("🆘 SUPPORT", url=f"https://t.me/{config.SUPPORT_USERNAME}")]
    ]

    await context.bot.send_message(
        chat_id=chat_id,
        text="🎬 Choose a category:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await check_joined(user_id, context):
        keyboard = [
            [InlineKeyboardButton("Join Channel 1", url=config.CHANNEL_1_LINK)],
            [InlineKeyboardButton("Join Channel 2", url=config.CHANNEL_2_LINK)],
            [InlineKeyboardButton("✅ Verify", callback_data="verify")]
        ]

        await update.message.reply_text(
            "⚠️ Join both channels first:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await send_menu(update.effective_chat.id, context)


# ---------------- SEND VIDEOS ----------------
async def send_videos(chat_id, context, category):
    data = {
        "indian": config.INDIAN,
        "viral": config.VIRAL,
        "russia": config.RUSSIA
    }[category]

    for msg_id in data:
        try:
            await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=config.STORAGE_CHANNEL,
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
        await query.message.edit_text("⚠️ Please join channels first.")
        return

    if data == "verify":
        await query.message.edit_text("✅ Verified!")
        await send_menu(query.message.chat_id, context)

    elif data in ["indian", "viral", "russia"]:
        await query.message.reply_text("📥 Sending videos...")
        await send_videos(query.message.chat_id, context, data)


# ---------------- MAIN ----------------
app = Application.builder().token(config.BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")
app.run_polling()