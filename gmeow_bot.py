import os
import json
import random
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

DATA_FILE = "gmeow_data.json"
TOKEN = os.getenv("7423055994:AAGyBcm2CYcKBurv8gDQVMF4E2QSLhWwarc")

REWARDS = [
    {"name": "Golden Hairball", "points": 100, "desc": "The mythical treasure of memecats."},
    {"name": "Used Sock", "points": 5, "desc": "It's warm... and suspiciously damp."},
    {"name": "Laser Pointer", "points": 10, "desc": "Distracting but fun!"},
    {"name": "Empty Box", "points": 0, "desc": "The real gift is disappointment."},
    {"name": "Tuna Can", "points": 30, "desc": "Vintage 2022. Smells divine."}
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

async def gmeow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Anonymous"
    today = datetime.utcnow().strftime('%Y-%m-%d')
    data = load_data()
    user = data.get(user_id, {"points": 0, "uses": {}})
    used_today = user["uses"].get(today, 0)

    if used_today >= 2:
        await update.message.reply_text("😿 You’ve already opened 2 boxes today!")
        return

    reward = random.choice(REWARDS)
    user["points"] += reward["points"]
    user["uses"][today] = used_today + 1
    data[user_id] = user
    save_data(data)

    await update.message.reply_text(f"🎁 You got: *{reward['name']}* ({reward['points']} pts)\n_{reward['desc']}_", parse_mode="Markdown")

async def mygmeow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    user = data.get(user_id, {"points": 0})
    await update.message.reply_text(f"🐾 Your Gmeow Points: {user['points']}")

async def gmeowtop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    leaderboard = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True)[:10]
    msg = "🏆 *Top 10 Gmeow Players:*\n"
    for i, (uid, user) in enumerate(leaderboard, 1):
        msg += f"{i}. {user.get('name', 'Unknown')} - {user['points']} pts\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("Gmeow", gmeow))
    app.add_handler(CommandHandler("mygmeow", mygmeow))
    app.add_handler(CommandHandler("Gmeowtop", gmeowtop))
    app.run_polling()
