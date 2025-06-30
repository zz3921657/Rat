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
