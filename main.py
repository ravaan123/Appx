import requests
import json
import subprocess
from pyrogram.types.messages_and_media import message
import helper
from pyromod import listen
from pyrogram.types import Message
import tgcrypto
import pyrogram
from pyrogram import Client, filters
import time
from pyrogram.types import User, Message
from p_bar import progress_bar
from subprocess import getstatusoutput
import logging
import os
import re

import requests
bot = Client(
    "CW",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

logger = logging.getLogger()
# thumb = os.environ.get("THUMB")
# if thumb.startswith("http://") or thumb.startswith("https://"):
#     getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
#     thumb = "thumb.jpg"

@bot.on_message(filters.command(["start"]))
async def start(bot, update):
       await update.reply_text("Hi i am **Careerwill Downloader**.\n\n"
                              "**NOW:-** "
                                       
                                       "first join here - @BOT_UPDATES_by_RAJ for command ..\n\n"
                                     "Bot made by **@Sccwaleyarr ...❤️‍🔥raj🥀**" )

ACCOUNT_ID = "6206459123001"
BCOV_POLICY = "BCpkADawqM1474MvKwYlMRZNBPoqkJY-UWm7zE1U769d5r5kqTjG0v8L-THXuVZtdIQJpfMPB37L_VJQxTKeNeLO2Eac_yMywEgyV9GjFDQ2LTiT4FEiHhKAUvdbx9ku6fGnQKSMB8J5uIDd"
bc_url = (
    f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
)
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

url="https://elearn.crwilladmin.com/api/v1/"

info= {
 "deviceType":"android",
    "password":"",
    "deviceModel":"Asus ASUS_X00TD",
    "deviceVersion":"Pie(Android 9.0)",
    "email":"",
}

@bot.on_message(filters.command("fuckcw"))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send ID & Password in this manner otherwise bot will not respond.\n\nSend like this:-  ID*Password"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text
    await input1.delete(True)
    try:
        if "*" in raw_text:
            em = raw_text.split("*")[0]
            ps = raw_text.split("*")[1]
            payload={ "deviceType": "android", "password": ps, "deviceIMEI": "", "deviceModel": "XiaoMi M2007J17C", "deviceVersion": "upper than 31", "email": em, "deviceToken": "eX1ixOOrRZuc7cUygJpdDl:APA91bGBGSGDyupdzriHH0Hi0yvOH6ID2jYFsxz0Y_RdFcAUUGsSJL-mNxKARjBC9zoyjQT-C0OD48It06MyahSYGwccvQ4TeQDKkSQ50jJAYHXKz3b_WdfQPBWlsn2GMOxFPSvxNyYw" }
            r = requests.post('https://elearn.crwilladmin.com/api/v5/login-other', headers=hdr, json=payload).json()
            rdata = r.get("data", {})
            token = rdata.get("token", '')
            await editable.edit(f"Login Successful")
        else:
            token = raw_text
    except Exception as e:
        await editable.edit(f"An error occurred during login: {e}")
        return

    headers = {
    'token': token,
    'usertype':'2',
    'appver':'86',
    'apptype':'android',
    'accept-encoding':'gzip',
    'user-agent':'okhttp/5.0.0-alpha.2'}

    url1 = requests.get('https://elearn.crwilladmin.com/api/v5/my-batch', headers=headers)
    keydata = json.loads(url1.text)
    print(keydata)
    data = keydata.get("data", {})
    bdata = data.get("batchData", [])
    print(bdata)

    if not bdata:
        await editable.edit("You don't have any batches available.")
        return

    cool = ""
    FFF = "BATCH-ID  -  BATCH NAME"
    for item in bdata:
        id = item.get("id")
        btchnam = item.get("batchName")
        print(btchnam)
        insname = item.get("instructorName")
        aa = f"{id} - {btchnam}-->{insname}\n\n"
        if len(f'{cool}{aa}') > 4096:
            cool = ""
        cool += aa
    await m.reply_text(f"Token for future use:\n\n {token}")
    await editable.edit(f'{"You have these batches :-"}\n\n{FFF}\n\n{cool}')
    editable1 = await m.reply_text("Now send the Batch ID to Download")

    input2 = await bot.listen(editable1.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    editable2 = await m.reply_text("📥Please wait patiently. 🧲Scraping Url...")
    url2 = requests.get(f"https://elearn.crwilladmin.com/api/v5/batch-topic/{raw_text2}?type=class", headers=headers)
    keydata2 = json.loads(url2.text)
    b_data = keydata2["data"]["batch_topic"]
    filename = keydata2["data"]["batch_detail"]["name"]
    
    unique_urls = [] 
    for topic in b_data:
        topicName = topic["topicName"]
        # T_ID = "&".join([topic["id"]])
        T_ID = "&".join([str(topic["id"])])
    
        topic_ids = T_ID.split('&')
    
        for u in topic_ids:
            url3 = requests.get(f"https://elearn.crwilladmin.com/api/v5/batch-detail/{raw_text2}?redirectBy=mybatch&topicId={u}&pToken=", headers=headers)
            keydata3 = json.loads(url3.text)
            razz = keydata3["data"]["class_list"]["classes"]
            razz.reverse()
            all_urls = ""
            try:
                for data in razz:
                    razid = data["id"]
                    lessonName = data["lessonName"].replace("/", "_")
                    lessonExt = data["lessonExt"]
                    url3 = requests.get(f"https://elearn.crwilladmin.com/api/v5/class-detail/{razid}", headers=headers)
                    lessonUrl = json.loads(url3.text)['data']['class_detail']['lessonUrl']
                    if lessonExt == 'brightcove':
                        ntr = requests.get(f"https://elearn.crwilladmin.com/api/v5/livestreamToken?type=brightcove&vid={razid}&module=batch", headers=headers)
                        master = json.loads(ntr.text)
                        st2mtok = master["data"]["token"]
                        link = bc_url + lessonUrl + "/master.m3u8?bcov_auth=" + st2mtok
                    elif lessonExt == 'youtube':
                        link = "https://www.youtube.com/embed/" + lessonUrl
                    cc = f"{lessonName}:{link}"
                    unique_urls.append(cc)  # Append to list to maintain order
                await editable2.edit(f"🧲**Scraping videos Url**: `{topicName}`")  # Display topic name only
            except Exception as e:
                print(str(e))

    try:
        url4 = requests.get(f"https://elearn.crwilladmin.com/api/v5/batch-notes/{raw_text2}?b_data={raw_text2}", headers=headers)
        pdfD = json.loads(url4.text)
        note = pdfD["data"]["notesDetails"]
        for data in note:
            name = data["docTitle"]
            s = data["docUrl"]
            cc = f"{name}:{s}"
            unique_urls.append(cc)  # Append to list to maintain order
    except Exception as e:
        print(str(e))
    
    # Write all unique URLs into one document file
    with open(f"{filename}.txt", 'w') as f:
        for url in unique_urls:
            f.write(url + '\n')
    
    await m.reply_document(
        document=f"{filename}.txt",
        caption=f"❤️‍🔥**APP Name**: Career Will\n🥀**Batch Name**: `{filename}`"
)
                     
                    
                
                
        
        
        


bot.run()
