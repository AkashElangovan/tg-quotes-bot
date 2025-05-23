# bot.py

import json
import random
from telegram import Bot
import os

# Replace these
BOT_TOKEN = ""
CHAT_ID = ""

bot = Bot(token=BOT_TOKEN)

# Load all notes
with open("notes.json", "r", encoding="utf-8") as f:
    notes = json.load(f)

all_keys = list(notes.keys())

# Load sent notes
sent_file = "sent_notes.json"
if os.path.exists(sent_file):
    with open(sent_file, "r", encoding="utf-8") as f:
        sent_notes = json.load(f)
else:
    sent_notes = []

# If all notes have been sent, reset
if len(sent_notes) >= len(all_keys):
    sent_notes = []

# Pick a random unsent note
remaining_notes = [key for key in all_keys if key not in sent_notes]
note_key = random.choice(remaining_notes)
note = notes[note_key]

# Format the message
message = (
    f"📘 *{note['Title']}*\n\n"
    f"🧠 *Explanation:*\n_{note['Explanation']}_\n\n"
    f"💡 *Example:*\n_{note['Example']}_"
)

# Send the message
bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

# Mark as sent
sent_notes.append(note_key)
with open(sent_file, "w", encoding="utf-8") as f:
    json.dump(sent_notes, f, indent=2)
