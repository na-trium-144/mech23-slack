#!/usr/bin/env python3
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv
load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
)

# 全員をチャンネルに招待する
def invite_all_impl(channel_id, say):
    print(f"invite_all to {channel_id}")
    try:
        member_list = app.client.users_list()
    except SlackApiError as e:
        print(f"Error: {e}")
        return
    try:
        app.client.conversations_join(channel=channel_id)
    except SlackApiError as e:
        print(f"Error: {e}")
    for m in member_list['members']:
        print(f"invite {m['id']}: {m['name']}")
        try:
            app.client.conversations_invite(channel=channel_id, users=[m['id']])
        except SlackApiError as e:
            print(f"Error: {e}")

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
    test_channel_id = "C04UNBSBRJT"
    try:
        app.client.chat_postMessage(
            channel=test_channel_id,
            text="アプリ起動しました"
        )
    except SlackApiError as e:
        print(f"Error: {e}")

    # app.start(port=int(os.environ.get("PORT", 3000)))
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
