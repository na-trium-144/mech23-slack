#!/usr/bin/env python3
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv
load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
)

def invite_all_impl(channel_id, say):
    say(f"チャンネルid={channel_id}")

@app.command("/inviteall")
def invite_all(ack, say, command):
    ack()
    print(command)
    invite_all_impl(command["channel_id"], say)
    
@app.event("app_mention")
def event_test(event, say):
    print(event)
    if "全員" in event["text"] and "招待" in event["text"]:
        invite_all_impl(event["channel"], say)
    else:
        say("Hello world!")

# Start your app
if __name__ == "__main__":
    # app.start(port=int(os.environ.get("PORT", 3000)))
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
