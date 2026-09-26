import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler,
                          CallbackQueryHandler, ContextTypes)
from config import BOT_TOKEN, ADMIN_ID
import database as db

def is_admin(uid): return uid == ADMIN_ID

def menu():
    kb = [
        [InlineKeyboardButton("⏰ Time", callback_data="time")],
        [InlineKeyboardButton("💬 Quote", callback_data="quote")],
        [InlineKeyboardButton("🪙 Coin Toss", callback_data="coin")],
    ]
    return InlineKeyboardMarkup(kb)

QUOTES = [
    "Jo hota hai achhe ke liye hota hai.",
    "Mehnat karo, phal ki chinta mat karo.",
    "Har din ek nayi shuruaat hai.",
    "Girna bura nahi, gir ke na uthna bura hai.",
]

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    db.add_user(u.id, u.username or "", u.first_name or "",
                datetime.now().isoformat())
    await update.message.reply_text(
        f"Namaste {u.first_name}! 👋\nMenu se chuno:",
        reply_markup=menu())

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "time":
        now = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        await q.edit_message_text(f"⏰ Abhi: {now}", reply_markup=menu())

    elif q.data == "quote":
        await q.edit_message_text(f"💬 {random.choice(QUOTES)}",
                                  reply_markup=menu())

    elif q.data == "coin":
        res = random.choice(["Heads 🪙", "Tails 🪙"])
        await q.edit_message_text(f"Result: {res}", reply_markup=menu())

# ---------- ADMIN ----------
async def admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("❌ Access denied")
    await update.message.reply_text(
        "🛠 Admin Panel\n"
        "/stats — total users\n"
        "/users — user ids\n"
        "/broadcast <msg> — sabko bhejo")

async def stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    await update.message.reply_text(f"👥 Total users: {db.user_count()}")

async def users(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    ids = db.all_users()
    await update.message.reply_text("IDs:\n" + "\n".join(map(str, ids)))

async def broadcast(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not ctx.args:
        return await update.message.reply_text("Use: /broadcast <message>")
    msg = " ".join(ctx.args)
    sent = 0
    for uid in db.all_users():
        try:
            await ctx.bot.send_message(uid, msg)
            sent += 1
        except Exception:
            pass
    await update.message.reply_text(f"✅ Bheja {sent} users ko")

def main():
    db.init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot chal raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()