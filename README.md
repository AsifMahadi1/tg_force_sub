# TG Force Subscribe Bot

A lightweight **force-subscribe** bot for Telegram groups. It deletes messages
from users who are **not** subscribed to a required channel and replies with a
**Subscribe** button.

> **Pure Python stdlib** — no `pip install`, no virtualenv. Only needs Python 3.

## Features

- ✅ Deletes messages from non-subscribers automatically
- ✅ Posts a reminder with an inline **Subscribe** button (auto-deleted after ~10s)
- ✅ Leaves group admins / channel posts alone
- ✅ Single file, zero dependencies
- ✅ Crash-loop runner (`run.sh`) for unattended operation

## Files

| File | Purpose |
|---|---|
| `bot.py` | The bot (single file, stdlib only) |
| `.env.example` | Template for credentials — copy to `.env` |
| `run.sh` | Crash-loop runner (auto-restarts if it exits) |
| `start.sh` | Start in the background (`nohup`) |
| `stop.sh` | Stop the background bot |

## Quick start

```bash
git clone https://github.com/AsifMahadi1/tg_force_sub.git
cd tg_force_sub
cp .env.example .env
# edit .env → set BOT_TOKEN and CHANNEL_USERNAME
bash start.sh
```

Stop:

```bash
bash stop.sh
```

Run in the foreground (live logs):

```bash
bash run.sh
```

## Configuration (`.env`)

```
BOT_TOKEN=123456:ABC...          # your bot token from @BotFather
CHANNEL_USERNAME=@yourchannel    # the channel users must join
```

## Setup on Telegram

1. Add the bot to your group as an **admin** with the *Delete messages* permission.
2. Make sure the bot is a member/admin of the required channel too, so it can
   check membership via `getChatMember`.
3. Set `CHANNEL_USERNAME` in `.env`.

## How it works

- On every group message it checks the sender's membership in `CHANNEL_USERNAME`
  (`getChatMember`).
- If the user is **not** a member / administrator / creator:
  - their message is deleted,
  - a reminder with a **Subscribe** button is posted (auto-deleted after ~10s).
- Group admins and channel posts are ignored.

## ⚠️ Security

- `.env` holds your **live bot token** and is git-ignored — never commit it.

## Requirements

- Python 3.6+
- Linux or macOS
- Internet access

## License

MIT
