import os
import json
import random
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# --- Config ---
BOT_TOKEN = os.environ["BOT_TOKEN"]
APP_URL = os.environ["APP_URL"]
PORT = int(os.environ.get("PORT", 10000))

NOTES_FILE = "notes.json"
SENT_FILE = "sent_notes.json"

# --- Load notes ---
with open(NOTES_FILE, "r", encoding="utf-8") as f:
    notes = json.load(f)

all_keys = list(notes.keys())

# --- Sent notes storage ---
def load_sent_notes():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_sent_notes(sent_notes):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(sent_notes, f)

def get_new_note():
    sent_notes = load_sent_notes()
    if len(sent_notes) >= len(all_keys):
        sent_notes = []
    remaining = [k for k in all_keys if k not in sent_notes]
    key = random.choice(remaining)
    sent_notes.append(key)
    save_sent_notes(sent_notes)
    note = notes[key]
    return (
        f"📘 *{note['Title']}*\n\n"
        f"🧠 *Explanation:*\n_{note['Explanation']}_\n\n"
        f"💡 *Example:*\n_{note['Example']}_"
    )

# --- Flask app ---
flask_app = Flask(__name__)

# --- Telegram bot ---
application = ApplicationBuilder().token(BOT_TOKEN).build()

# /new command
async def new_note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = get_new_note()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')

application.add_handler(CommandHandler("new", new_note_command))

# Webhook route
@flask_app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

@flask_app.route("/")
def home():
    return "Bot is running!"

# Auto-send every 3 hours
async def auto_send_note(context: ContextTypes.DEFAULT_TYPE):
    chat_id = os.environ.get("CHAT_ID")
    if not chat_id:
        print("CHAT_ID not set.")
        return
    msg = get_new_note()
    await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')

# --- Start everything ---
if __name__ == "__main__":
    import threading

    async def post_init(application):
        # Set webhook
        await application.bot.set_webhook(url=f"{APP_URL}/{BOT_TOKEN}")
        # Schedule auto-send job every 3 hours
        application.job_queue.run_repeating(auto_send_note, interval=3 * 60 * 60, first=10)

    application.post_init = post_init

    # Run Flask in a separate thread
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=PORT), daemon=True).start()

    # Run bot polling loop (no asyncio.run)
    application.run_polling()
