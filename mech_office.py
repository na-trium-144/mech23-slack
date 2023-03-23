#!/usr/bin/env python
# coding: utf-8

# In[10]:


from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os


# In[1]:


import requests


# In[14]:


from bs4 import BeautifulSoup


# In[28]:


from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# In[5]:


session = requests.session()


# In[11]:


payload = {
    "password_protected_pwd": os.environ.get("OFFICE_LOGIN_PASSWD"),
    "wp-submit": "ログイン",
    "password_protected_cookie_test": 1,
    "password-protected": "login",
    "redirect_to": os.environ.get("OFFICE_URL"),
}
res = session.post(os.environ.get("OFFICE_LOGIN_URL"), data=payload)


# In[15]:


soup = BeautifulSoup(res.text, 'html.parser')


# In[27]:


parsed_posts = []
for post in soup.select(".post"):
    parsed_posts.append({
        "pid": post["id"],
        "title": post.select_one(".post-title").a.get_text(),
        "href": post.select_one(".post-title").a["href"],
        "content": post.select_one(".post-content").get_text(" "),
    })
# print(parsed_posts)


# In[29]:


client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


# In[44]:


channel_id = "C04UNBSBRJT"
channel_id_notice = "C04VCJWTVFE"


# In[45]:


for post in parsed_posts:
    new_post = f"<{post['href']}|*{post['title']}*>\n\n{post['content']}"
    prev_post = ""
    filename = f"./{post['pid']}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            prev_post = f.read()
    with open(filename, "w") as f:
        f.write(new_post)
    try:
        if new_post != prev_post:
            result = client.chat_postMessage(
                channel=channel_id,
                text=f"{post['pid']} changed"
            )
            result = client.chat_postMessage(
                channel=channel_id_notice,
                text=new_post
            )
        else:
            result = client.chat_postMessage(
                channel=channel_id,
                text=f"{post['pid']} not changed"
            )
    except SlackApiError as e:
        print(f"Error: {e}")

