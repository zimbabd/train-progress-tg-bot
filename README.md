# Train Progress Telegram Bot

A Telegram bot for recording workouts and viewing recent or PDF training statistics.

Bot: [@TrainProgress_bot](https://t.me/TrainProgress_bot)

## Features

- Record running, squats, push-ups, planks, and jump-rope workouts.
- View the five most recent workouts.
- Export workout history as a PDF.
- Store user and workout data in a local SQLite database.

## Requirements

- Python 3.10 or newer
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Setup

Run the following commands from the project root.

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `bot_token.txt` file in the project root and put only your BotFather token in it. The file is excluded from Git. Never commit or share the token; revoke it with BotFather if it has been exposed.

## Run

From the project root, with the virtual environment activated:

```bash
python main.py
```

The SQLite database is created automatically at `data/tgbot_db.db`. It is local application data and excluded from Git. Back it up separately if you need to preserve workout records.

## Bot commands

- `/start` — register and open the bot menu
- `/training` — record a workout
- `/statistics` — view recent workouts or export all statistics as PDF
- `/support` — show the support contact

## Project layout

```text
.
├── config.py       # Local paths for the token and database
├── main.py         # Bot entry point
├── exercises/      # Workout input flows
├── handlers/       # Telegram commands and callbacks
├── model/          # Data models
├── repository/     # SQLite access
├── utils/          # PDF report generation
└── fonts/          # Font used in PDF reports
```

## Security

Never commit bot tokens, local databases, virtual environments, or generated reports. The repository's `.gitignore` excludes these files.
