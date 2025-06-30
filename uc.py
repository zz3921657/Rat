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

# --- /buy_uc ---
async def buy_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# --- /buy_uc ---
async def buy_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
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

# --- /start or /buy_uc ---
async def buy_uc(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# --- User selects a price ---
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

# --- User enters UID ---
async def get_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()

    if not uid.isdigit():
        await update.message.reply_text("⚠️ Invalid UID. Please enter **numbers only**.", parse_mode="Markdown")
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

# --- Callback query handler ---
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

    elif data.startswith("approve_") or data.startswith("reject_"):
        order_id = int(data.split("_")[1])
        order = ORDER_LOG[order_id]
        user_id = order["user_id"]

        if data.startswith("approve_"):
            await context.bot.send_message(chat_id=user_id, text="✅ Your UC order has been *approved* by admin!", parse_mode="Markdown")
            await query.message.reply_text("✅ Order approved.")
        else:
            await context.bot.send_message(chat_id=user_id, text="❌ Your UC order has been *rejected* by admin.", parse_mode="Markdown")
            await query.message.reply_text("❌ Order rejected.")
        return ConversationHandler.END

# --- Screenshot received ---
async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = update.message.photo[-1].file_id
        user = update.effective_user

        order = {
            "user_id": user.id,
            "username": user.username,
            "name": user.first_name,
            "package": context.user_data["package"],
            "amount": context.user_data["amount"],
            "uid": context.user_data["uid"],
            "photo_id": photo
        }

        ORDER_LOG.append(order)
        order_id = len(ORDER_LOG) - 1

        caption = (
            f"📥 *New UC Order Received!*\n\n"
            f"👤 User: {user.first_name} (@{user.username})\n"
            f"🪙 Package: {order['package']}\n"
            f"💰 Amount: ₹{order['amount']}\n"
            f"🎮 UID: `{order['uid']}`\n"
            f"🆔 Order ID: #{order_id}"
        )

        buttons = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{order_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{order_id}")
            ]
        ]

        await context.bot.send_photo(
            chat_id=ADMIN_USER_ID,
            photo=photo,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        await update.message.reply_text("✅ Screenshot received. Please wait for admin confirmation.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("⚠️ Please send a valid *screenshot photo*.", parse_mode="Markdown")
        return GET_SCREENSHOT

# --- Main ---
def main():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("7552538341:AAGAqvdJarpYs09e_cU0qrFAUFbPv4vpih8")  # Make sure to define BOT_TOKEN in .env

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", buy_uc), CommandHandler("buy_uc", buy_uc)],
        states={
            CHOOSE_PRICE: [CallbackQueryHandler(choose_price)],
            GET_UID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_uid)],
            ORDER_CONFIRM: [CallbackQueryHandler(handle_callback)],
            GET_SCREENSHOT: [MessageHandler(filters.PHOTO, get_screenshot)],
        },
        fallbacks=[CallbackQueryHand]()
