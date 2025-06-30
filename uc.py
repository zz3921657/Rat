from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters, ContextTypes
)

# --- States ---
CHOOSE_PRICE, GET_UID, ORDER_CONFIRM, GET_SCREENSHOT = range(4)

# --- Admin ID ---
ADMIN_USER_ID = 6829160614

# --- UC Options ---
PRICE_OPTIONS = {
    "300 UC – ₹200": ("325 UC", 200),
    "600 UC – ₹400": ("660 UC", 400),
    "3000 UC – ₹1250": ("1800 UC", 1250),
    "6000 UC – ₹2800": ("6000 UC", 2800),
    "12000 UC – ₹5200": ("12000 UC", 5200)
}

# --- QR Image ---
QR_IMAGE_PATH = "1000020718.png"

# --- Order Log ---
ORDER_LOG = []

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "Player"

    welcome_text = (
        f"👋 Hey *『𝙽𝙾1』{name}★!*,\n"
        f"🎉 Welcome to the *CARDING UC Bot!* 💥\n\n"
        f"✨ We're thrilled to have you here. Let's get you started.\n\n"
        f"💰 Please select your desired UC package below 👇"
    )

    keyboard = [[InlineKeyboardButton(text, callback_data=text)] for text in PRICE_OPTIONS]
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSE_PRICE

# --- UC Pack Selected ---
async def choose_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected = query.data
    context.user_data["selected_price"] = selected
    context.user_data["package"], context.user_data["amount"] = PRICE_OPTIONS[selected]

    msg = (
        f"You selected *{selected}*.\n\n"
        f"Now, please send your *Game UID*."
    )

    buttons = [
        [
            InlineKeyboardButton("🔁 Back to Menu", callback_data="back_to_menu"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_order")
        ]
    ]

    await query.message.reply_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))
    return GET_UID

# --- Handle UID ---
async def get_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()

    if not uid.isdigit():
        await update.message.reply_text("⚠️ Invalid UID. Please enter **numbers only**.")
        return GET_UID

    context.user_data["uid"] = uid

    summary = (
        f"📦 *Order Summary:*\n\n"
        f"🪙 UC Package: {context.user_data['package']}\n"
        f"💰 Amount: ₹{context.user_data['amount']}\n"
        f"🎮 Your Game ID: `{uid}`\n\n"
        f"Please confirm these details before proceeding."
    )

    buttons = [
        [InlineKeyboardButton("✅ Confirm & Proceed to Payment", callback_data="confirm_order")],
        [InlineKeyboardButton("❌ Cancel Order", callback_data="cancel_order")]
    ]

    await update.message.reply_text(summary, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))
    return ORDER_CONFIRM

# --- Handle Callback Queries ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "confirm_order":
        import os
        if not os.path.exists(QR_IMAGE_PATH):
            await query.message.reply_text("⚠️ QR image not found.")
            return CHOOSE_PRICE

        await query.message.reply_photo(
            photo=open(QR_IMAGE_PATH, 'rb'),
            caption="📲 *Scan this QR to pay.*\n\nAfter payment, please send the screenshot below 👇\n\n📞 Contact support: @Heyynitin",
            parse_mode="Markdown"
        )
        return GET_SCREENSHOT

    elif data == "cancel_order":
        await query.message.reply_text("❌ Your order was cancelled.\n\n💰 You can start a new order below 👇")

        keyboard = [[InlineKeyboardButton(text, callback_data=text)] for text in PRICE_OPTIONS]
        await query.message.reply_text("Please select a UC package:", reply_markup=InlineKeyboardMarkup(keyboard))
        return CHOOSE_PRICE

    elif data == "back_to_menu":
        keyboard = [[InlineKeyboardButton(text, callback_data=text)] for text in PRICE_OPTIONS]
        await query.message.reply_text("💰 Please select a UC package again:", reply_markup=InlineKeyboardMarkup(keyboard))
        return CHOOSE_PRICE

# --- Screenshot Upload ---
async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = update.message.photo[-1].file_id
        caption = (
            f"🧾 *New UC Order!*\n"
            f"👤 @{update.effective_user.username or 'unknown'}\n"
            f"🎮 UID: `{context.user_data.get('uid')}`\n"
            f"📦 Package: {context.user_data.get('package')}\n"
            f"💰 Amount: ₹{context.user_data.get('amount')}"
        )

        # Send to Admin
        await context.bot.send_photo(chat_id=ADMIN_USER_ID, photo=photo, caption=caption, parse_mode="Markdown")

        # Save order
        ORDER_LOG.append({
            "username": update.effective_user.username or "unknown",
            "uid": context.user_data.get("uid"),
            "package": context.user_data.get("package"),
            "amount": context.user_data.get("amount")
        })

        # Thank user
        await update.message.reply_text("🎉 Thank you for your purchase!\nWe'll confirm and deliver shortly.\n\n💰 Want to buy more UC? Choose a package below 👇")

        keyboard = [[InlineKeyboardButton(text, callback_data=text)] for text in PRICE_OPTIONS]
        await update.message.reply_text("Choose another UC pack:", reply_markup=InlineKeyboardMarkup(keyboard))
        return CHOOSE_PRICE
    else:
        await update.message.reply_text("⚠️ Please send the screenshot as an image.")
        return GET_SCREENSHOT

# --- Admin Dashboard ---
async def admin_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("🚫 You are not authorized to access the admin dashboard.")
        return

    if not ORDER_LOG:
        await update.message.reply_text("📭 No orders yet.")
        return

    total_orders = len(ORDER_LOG)
    total_revenue = sum(order["amount"] for order in ORDER_LOG)

    msg = (
        f"🛠️ *Admin Dashboard*\n\n"
        f"📦 Total Orders: {total_orders}\n"
        f"💰 Total Revenue: ₹{total_revenue}\n\n"
        f"🧾 *Recent Orders:*\n"
    )

    recent_orders = ORDER_LOG[-5:]
    for i, order in enumerate(recent_orders[::-1], 1):
        msg += (
            f"\n{i}. 👤 @{order['username']}\n"
            f"   🎮 UID: `{order['uid']}`\n"
            f"   📦 {order['package']} – ₹{order['amount']}\n"
        )

    await update.message.reply_text(msg, parse_mode="Markdown")

# --- Help Command ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "ℹ️ *Bot Commands Help*\n\n"
        "/BUY UC – Begin your UC order process\n"
        "/help – Show this help message\n"
        "/admin – Admin dashboard (Admin only)\n\n"
        "🔹 Just follow the steps guided by the bot to purchase UC.\n"
        "🔹 If you face issues, contact support: @Heyynitin"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# --- Main ---
if __name__ == "__main__":
    app = ApplicationBuilder().token("7552538341:AAGAqvdJarpYs09e_cU0qrFAUFbPv4vpih8").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("BUY UC", BUY UC)],
        states={
            CHOOSE_PRICE: [CallbackQueryHandler(choose_price)],
            GET_UID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_uid),
                CallbackQueryHandler(handle_callback)
            ],
            ORDER_CONFIRM: [CallbackQueryHandler(handle_callback)],
            GET_SCREENSHOT: [MessageHandler(filters.PHOTO, get_screenshot)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("admin", admin_dashboard))
    app.add_handler(CommandHandler("help", help_command))

    print("✅ Bot is running...")
    app.run_polling()
