#!/usr/bin/env python3
"""Force-subscribe bot — pure stdlib, no external deps.

Adds the bot to a group as admin; deletes messages from users who are not
subscribed to the required channel and posts a Subscribe button.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "").strip()  # e.g. @newspediabd
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
REQUIRED_STATUSES = {"member", "administrator", "creator"}
REMINDER_TEXT = "🚫 To send messages in this group, you must subscribe first."
REMINDER_TTL = 10  # seconds


def call(method, **params):
    url = f"{API}/{method}"
    data = json.dumps(params).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read())
        except Exception:
            return {"ok": False, "description": str(e)}
    except Exception as e:
        return {"ok": False, "description": str(e)}


def is_subscribed(user_id):
    res = call("getChatMember", chat_id=CHANNEL_USERNAME, user_id=user_id)
    if not res.get("ok"):
        return False
    status = res["result"].get("status", "")
    return status in REQUIRED_STATUSES


def handle(message):
    chat = message.get("chat", {})
    if chat.get("type") not in ("group", "supergroup"):
        return
    user = message.get("from") or {}
    user_id = user.get("id")
    if not user_id:
        return
    # leave admins/owners of the group alone
    if message.get("sender_chat"):
        return
    if is_subscribed(user_id):
        return

    chat_id = chat["id"]
    call("deleteMessage", chat_id=chat_id, message_id=message["message_id"])

    link = CHANNEL_USERNAME.lstrip("@")
    res = call(
        "sendMessage",
        chat_id=chat_id,
        text=REMINDER_TEXT,
        reply_markup={
            "inline_keyboard": [
                [{"text": "Subscribe", "url": f"https://t.me/{link}"}]
            ]
        },
    )
    if res.get("ok"):
        msg_id = res["result"]["message_id"]
        # remember for cleanup on next loop iteration
        PENDING_DELETES.append((time.time() + REMINDER_TTL, chat_id, msg_id))


PENDING_DELETES = []


def run_cleanup():
    now = time.time()
    for item in list(PENDING_DELETES):
        when, chat_id, msg_id = item
        if now >= when:
            call("deleteMessage", chat_id=chat_id, message_id=msg_id)
            PENDING_DELETES.remove(item)


def main():
    if not BOT_TOKEN or not CHANNEL_USERNAME:
        sys.exit("Missing BOT_TOKEN or CHANNEL_USERNAME env")

    me = call("getMe")
    if not me.get("ok"):
        sys.exit(f"Bad token: {me.get('description')}")
    print(f"Bot @{me['result']['username']} running for {CHANNEL_USERNAME}", flush=True)

    offset = None
    while True:
        try:
            params = {"timeout": 25, "allowed_updates": json.dumps(["message"])}
            if offset is not None:
                params["offset"] = offset
            url = f"{API}/getUpdates?{urllib.parse.urlencode(params)}"
            with urllib.request.urlopen(url, timeout=35) as r:
                data = json.loads(r.read())
            if not data.get("ok"):
                print("getUpdates error:", data.get("description"), flush=True)
                time.sleep(3)
                continue
            for upd in data["result"]:
                offset = upd["update_id"] + 1
                msg = upd.get("message")
                if msg:
                    handle(msg)
        except Exception as e:
            print("loop error:", e, flush=True)
            time.sleep(3)
        run_cleanup()


if __name__ == "__main__":
    main()
