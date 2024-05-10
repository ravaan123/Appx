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
                                       
                                       "first join here - @Hemendraa148 for command ..\n\n"
                                     "Bot made by **@Diftann...『𝗛𝗘𝗠𝗨』❤️🌚**" )

async def fetch_data(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json()
    
def decrypt_link(link):
    try:
        decoded_link = base64.b64decode(link)
        key = b'638udh3829162018'
        iv = b'fedcba9876543210'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_link = unpad(cipher.decrypt(decoded_link), AES.block_size).decode('utf-8')
        return decrypted_link
    except ValueError as ve:
        print(f"Padding error while decrypting link: {ve}")
    except Exception as e:
        print(f"Error decrypting link: {e}")

@bot.on_message(filters.command("hemu"))
async def handle_appxv2_logic(bot: bot, m: Message, api_endpoint: str):
    editable = await m.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    input1 = await bot.listen(editable.chat.id)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'auth-key': 'appxapi',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    raw_text = input1.text
        # Extracting opponent's user ID
    user_id = input1.from_user.id
    print("Opponent's user_id:", user_id)
    await input1.delete(True)
    email, password = raw_text.split("*")
    payload = {"email": email, "password": password}
    url = f"https://{api_endpoint}/post/userLogin?extra_details=0"
    print(f"Modified Login Url :- {url}")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            login = await response.json()
            print(f"Login Resp:- {login}")
            login_data = login.get("data", {})
            userid = login_data.get("userid", '')
            token = login_data.get("token", '')
            hdr1 = {
                'auth-key':'appxapi',
                'authorization': token,
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'en-US,en;q=0.9'
            }
            await editable.edit("**login Successful**")
            res1 = await fetch_data(session, f"https://{api_endpoint}/get/mycourse?userid={userid}", headers=hdr1)
            bdetail = res1.get("data", [])
            cool = ""
            FFF = "**BATCH-ID -      BATCH NAME **"
            for item in bdetail:
                id = item.get("id")
                batch = item.get("course_name")
                aa = f" `{id}`      - **{batch}**\n\n"
                if len(f'{cool}{aa}') > 4096:
                    print(aa)
                    cool = ""
                cool += aa
            await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
            editable1 = await m.reply_text("**Now send the Batch ID to Download**")
            print("user_id:", m.from_user.id)
            print("AUTH_USERS:", AUTH_USERS)

            if user_id is not None and user_id not in AUTH_USERS:
                print("User ID not in AUTH_USERS")

                await m.reply("**PLEASE UPGRADE YOUR PLAN**", quote=True)
                return
            else:
                   # Continue with the rest of your code here
                input2 = await bot.listen(editable.chat.id)
                raw_text2 = input2.text
                bname = next((x['course_name'] for x in bdetail if str(x['id']) == raw_text2), None)
                await input2.delete(True)
                await editable.delete()
                await editable1.delete()
                editable2 = await m.reply_text("📥**Please wait patiently. I'll take 2-5 minutes only** 🧲    `Scraping Url...`")
                res2 = await fetch_data(session, f"https://{api_endpoint}/get/allsubjectfrmlivecourseclass?courseid={raw_text2}&start=-1", headers=hdr1)
                subject = res2.get("data", [])
                subjID = "&".join([id["subjectid"] for id in subject])
                print(f'All Subject Id Info: {subjID}')
                subject_ids = subjID.split('&')
                all_urls = ""
                for u in subject_ids:
                    res3 = await fetch_data(session, f"https://{api_endpoint}/get/alltopicfrmlivecourseclass?courseid={raw_text2}&subjectid={u}&start=-1", headers=hdr1)
                    topic = res3.get("data", [])
                    topicids = "&".join([id["topicid"] for id in topic])
                    print(f"All topic ids Info : {topicids}")
                    topicid = topicids.split('&')
                    for t in topicid:
                        try:
                            res4 = await fetch_data(session, f"https://{api_endpoint}/get/livecourseclassbycoursesubtopconceptapiv3?courseid={raw_text2}&subjectid={u}&topicid={t}&start=-1&conceptid=", headers=hdr1)
                            videodata = res4.get("data", [])
                            for item in videodata:
                                pdf_link = item.get("pdf_link", "").replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").replace("ZmVkY2JhOTg3NjU0MzIxMA", "")
                                download_link = item.get("download_link", "").replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").replace("ZmVkY2JhOTg3NjU0MzIxMA", "")
                                name = item["Title"]
                                content_type = item.get("material_type", "")
                                if content_type == "VIDEO":
                                    if pdf_link:  # Check if pdf_link exists
                                        decrypted_pdf_link = decrypt_link(pdf_link)
                                        decrypted_video_link = decrypt_link(download_link)
                                        cc0 = f"{name} - Video: {decrypted_video_link}\n{name} - PDF: {decrypted_pdf_link}"
                                    else:
                                        decrypted_video_link = decrypt_link(download_link)
                                        cc0 = f"{name} - Video: {decrypted_video_link}"
                                elif content_type == "PDF":
                                    decrypted_pdf_link = decrypt_link(pdf_link)
                                    cc0 = f"{name} - PDF: {decrypted_pdf_link}"
                                all_urls += cc0 + '\n'
                        except asyncio.exceptions.TimeoutError:
                            print("Timeout error: The server took too long to respond.")
                            await m.reply(f"Timeout error: The server took too long to respond. Please Use Indian Proxy")
                if all_urls:
                    with open(f"{bname}.txt", 'w', encoding='utf-8') as f:
                        f.write(all_urls)
                await editable2.edit("Scraping completed successfully!")
                await editable2.delete(True)
                await m.reply_document(
                    document=f"{bname}.txt",
                    caption=f"✅** TEXT FILE **✅\n📍**APP Name**: Appx\n🔰**Batch Name**: `{bname}`"
        )


bot.run()
