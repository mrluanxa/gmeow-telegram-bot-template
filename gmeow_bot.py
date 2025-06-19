from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random, datetime, json, os

# Cấu trúc dữ liệu người chơi
user_data = {}

# Danh sách phần thưởng
rewards = [
    {"name": "Old Yarn Ball", "desc": "Still good... maybe.", "points": 1},
    {"name": "7-day-old Fish", "desc": "A bit smelly but still edible.", "points": 2},
    {"name": "Gmeow Rap CD", "desc": "Don't ever listen to it.", "points": 3},
    {"name": "Falling Soap", "desc": "Drama everywhere!", "points": 3},
    {"name": "First GMEOW Coin", "desc": "Plastic but precious.", "points": 4},
    {"name": "Laptop Miner", "desc": "Mining with MS Paint!", "points": 5},
    {"name": "Moon Ticket", "desc": "One way only!", "points": 6},
    {"name": "Dice of Fate", "desc": "You rolled a 9!", "points": 7},
    {"name": "Gmeow Trolled You", "desc": "No reward, just a smile.", "points": 0},
    {"name": "Gmeow on Fire!", "desc": "Super rare!", "points": 10},
]

def load_data():
    global user_data
    if os.path.exists("gmeow_data.json"):
        with open("gmeow_data.json", "r") as f:
            user_data = json.load(f)

def save_data():
    with open("gmeow_data.json", "w") as f:
        json.dump(user_data, f)

def reset_weekly_scores():
    for user in user_data.values():
        user["score"] = 0
    save_data()

def get_today():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')

async def gmeow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    today = get_today()

    if uid not in user_data:
        user_data[uid] = {"username": user.username or user.first_name, "score": 0, "last": today, "count": 0}
    if user_data[uid]["last"] != today:
        user_data[uid]["last"] = today
        user_data[uid]["count"] = 0

    if user_data[uid]["count"] >= 2:
        await update.message.reply_text("🐾 You've used all your boxes for today. Come back tomorrow, meow!")
        return

    reward = random.choice(rewards)
    user_data[uid]["score"] += reward["points"]
    user_data[uid]["count"] += 1
    save_data()

    msg = f"🎁 You got: *{reward['name']}*\n_{reward['desc']}_\nPoints: +{reward['points']}\n\n🐱 Total this week: {user_data[uid]['score']} pts"
    await update.message.reply_markdown(msg)

async def gmeowtop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = sorted(user_data.values(), key=lambda x: x['score'], reverse=True)[:10]
    msg = "🏆 *Gmeow Weekly Leaderboard:*\n"
    for i, user in enumerate(top, 1):
        msg += f"{i}. {user['username']} — {user['score']} pts\n"
    await update.message.reply_markdown(msg)

async def mygmeow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    today = get_today()
    if uid not in user_data:
        await update.message.reply_text("You haven't opened any boxes yet today.")
        return
    user = user_data[uid]
    left = max(0, 2 - user["count"]) if user["last"] == today else 2
    msg = f"😺 Your Gmeow Stats:\n• Weekly Score: {user['score']} pts\n• Boxes Opened Today: {user['count']}/2\n• Remaining: {left} box(es)"
    await update.message.reply_text(msg)

if __name__ == "__main__":
    load_data()
    app = ApplicationBuilder().token("7423055994:AAGyBcm2CYcKBurv8gDQVMF4E2QSLhWwarc").build()
    app.add_handler(CommandHandler("Gmeow", gmeow))
    app.add_handler(CommandHandler("Gmeowtop", gmeowtop))
    app.add_handler(CommandHandler("mygmeow", mygmeow))
    print("Bot is running...")
    app.run_polling()
