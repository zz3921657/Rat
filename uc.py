import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from collections import defaultdict

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your actual bot token
BOT_TOKEN = "7552538341:AAGAqvdJarpYs09e_cU0qrFAUFbPv4vpih8"

# Replace with your Telegram user ID(s)
ADMINS = [6829160614]  # Add your Telegram user ID here

# In-memory user data
user_points = defaultdict(int)
user_referrals = defaultdict(set)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    referred_by = None

    if context.args:
        referred_by = context.args[0]
        if referred_by != str(user_id):
            user_referrals[referred_by].add(user_id)
            user_points[referred_by] += 100  # Referral bonus

    welcome_text = (
        "👑 Welcome to *UC King Bot*! 👑\n\n"
        "🎮 Earn and redeem PUBG Unknown Cash (UC) through giveaways and rewards!\n\n"
        "💰 Use /prize to see current UC prizes.\n"
        "👥 Use /refer to invite friends and earn points.\n"
        "📊 Use /points to check your balance.\n"
    )

    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def prize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🏆 *UC Prize List:*\n\n"
        "🥉 60 UC  - 500 points\n"
        "🥈 300 UC - 2000 points\n"
        "🥇 600 UC - 3500 points\n"
        "👑 1800 UC - 7000 points\n\n"
        "💡 Earn points by referring friends or joining events!\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot_username = (await context.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"
    await update.message.reply_text(
        f"👥 *Refer & Earn*\n\n"
        f"Share this link with your friends:\n"
        f"{referral_link}\n\n"
        f"🎁 You’ll earn *100 points* for each signup!",
        parse_mode="Markdown",
    )


async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    points = user_points[user_id]
    referrals = len(user_referrals[user_id])
    await update.message.reply_text(
        f"📊 *Your Stats:*\n\n"
        f"⭐ Points: *{points}*\n"
        f"👥 Referrals: *{referrals}*",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 *Bot Commands:*\n\n"
        "/start - Begin or refer\n"
        "/prize - View prize list\n"
        "/refer - Get your referral link\n"
        "/points - Check your points\n"
        "/help - Show this help message",
        parse_mode="Markdown",
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("🚫 You are not authorized to access this dashboard.")
        return

    total_users = len(set(user_points.keys()) | set(user_referrals.keys()))
    total_points = sum(user_points.values())
    total_referrals = sum(len(refs) for refs in user_referrals.values())

    # Top 5 referrers
    leaderboard = sorted(user_referrals.items(), key=lambda x: len(x[1]), reverse=True)[:5]
    leaderboard_text = "\n".join(
        [f"👤 `{uid}` - {len(refs)} referrals" for uid, refs in leaderboard]
    ) or "No referrals yet."

    admin_text = (
        f"🛠 *Admin Dashboard*\n\n"
        f"👥 Total Users: *{total_users}*\n"
        f"🏅 Total Points Given: *{total_points}*\n"
        f"🔗 Total Referrals: *{total_referrals}*\n\n"
        f"📈 *Top Referrers:*\n{leaderboard_text}"
    )

    await update.message.reply_text(admin_text, parse_mode="Markdown")


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prize", prize))
    app.add_handler(CommandHandler("refer", refer))
    app.add_handler(CommandHandler("points", points))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("admin", admin))

    print("🤖 Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
