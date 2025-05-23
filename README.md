# Telegram Law & Bias Notes Bot

A lightweight Telegram bot that sends formatted notes from a JSON file containing laws and cognitive biases twice a day (8 AM and 8 PM IST).
The bot ensures each note is sent only once before cycling through all notes again.

---

## Features

-   Sends one note twice a day at 8 AM and 8 PM IST.
-   Cycles through all notes in the JSON before repeating any.
-   Proper message formatting with title, explanation, and example.
-   Simple, minimal dependencies.
-   Designed for deployment on [PythonAnywhere](https://www.pythonanywhere.com/) free tier with a single scheduled task running every 12 hours.

---

## Project Structure

```
.
├── bot.py
├── notes.json
├── sent_tracker.json
├── README.md
```

-   `bot.py` — Main bot script.
-   `notes.json` — JSON file with notes to send.
-   `sent_tracker.json` — Tracks which notes have been sent in the current cycle.
-   `README.md` — This file.

---

## Setup Instructions

### 1. Create Telegram Bot & Get Token

-   Talk to [@BotFather](https://t.me/BotFather) on Telegram.
-   Use `/newbot` command and follow instructions.
-   Copy your bot token (a string like `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).

### 2. Prepare your JSON file (`notes.json`)

Example format:

```json
{
  "Cognitive Dissonance": {
    "Title": "Cognitive Dissonance",
    "Explanation": "This occurs when we hold two conflicting beliefs, leading to discomfort. To reduce this discomfort, we might change one of our beliefs.",
    "Example": "You believe all rich people are greedy, but you also want to be rich. This creates dissonance, potentially leading you to rationalize that you don't truly want to be rich or to change your belief about rich people."
  },
  "The Spotlight Effect": {
    "Title": "The Spotlight Effect",
    "Explanation": "This is the tendency to overestimate how much other people are noticing our appearance, actions, or mistakes.",
    "Example": "You arrive late to the office and feel like everyone is judging you, even though they are likely focused on their own tasks."
  }
}
```

### 3. Write the Bot Script (`bot.py`)

Uses `python-telegram-bot==13.15`.
Reads and tracks sent notes in `sent_tracker.json`.
Sends a note at each run cycling through all notes before repeating.
Formats messages clearly with title, explanation, and example.

### 4. Install Dependencies Locally

```bash
pip install python-telegram-bot==13.15
```

### 5. Upload Files to PythonAnywhere

Upload `bot.py`, `notes.json`, and `sent_tracker.json` (create empty JSON `{}` if not exists) via PythonAnywhere dashboard.

Set up a scheduled task on PythonAnywhere to run the bot script every 12 hours at 8 AM and 8 PM IST.

Use the command:

```arduino
python3.10 /home/yourusername/bot.py
```

Adjust Python version if needed (3.10 recommended).

### 6. Running the Bot

Each scheduled run sends the next note in your JSON to your Telegram user/chat.

Notes cycle continuously without repetition until all have been sent.

Message formatting example sent:

```vbnet
*Title: Cognitive Dissonance*

Explanation: This occurs when we hold two conflicting beliefs, leading to discomfort. To reduce this discomfort, we might change one of our beliefs.

Example: You believe all rich people are greedy, but you also want to be rich. This creates dissonance, potentially leading you to rationalize that you don't truly want to be rich or to change your belief about rich people.
```

### 7. Important Tips

-   Make sure your bot token is securely stored — do **NOT** hardcode it in **bot.py** if you plan to share publicly. Use environment variables or config files.
-   Use Python **3.10** on PythonAnywhere since `python-telegram-bot==13.15` is not compatible with Python 3.13.
-   To reset the cycle manually, clear **sent_tracker.json** content (`{}`).
