import json
import random
import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace these
BOT_TOKEN = ""
CHAT_ID = ""  # optional check

# Paths
NOTES_FILE = "notes.json"
SENT_FILE = "sent_notes.json"

# Load all notes
with open(NOTES_FILE, "r", encoding="utf-8") as f:
    notes = json.load(f)

all_keys = list(notes.keys())


def load_sent_notes():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_sent_notes(sent_notes):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(sent_notes, f, indent=2)


def get_new_note():
    sent_notes = load_sent_notes()

    # Reset if all notes are sent
    if len(sent_notes) >= len(all_keys):
        sent_notes = []

    remaining_notes = [key for key in all_keys if key not in sent_notes]
    note_key = random.choice(remaining_notes)
    note = notes[note_key]

    sent_notes.append(note_key)
    save_sent_notes(sent_notes)

    # Format message
    message = (
        f"📘 *{note['Title']}*\n\n"
        f"🧠 *Explanation:*\n_{note['Explanation']}_\n\n"
        f"💡 *Example:*\n_{note['Example']}_"
    )

    return message


def new_note_command(update: Update, context: CallbackContext):
    message = get_new_note()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')


def main():
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add /new command handler
    dispatcher.add_handler(CommandHandler("new", new_note_command))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
