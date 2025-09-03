import os
import zipfile
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from google import genai

# -------------------------------
# Config
# -------------------------------
STRING_SESSION = "1BVtsOJYBu6Q_ffxWIB4ryDewg6rZ7BREPxvd54Cvu6j2naSg7TZ4C2Vc-UDTCH3_fiES3j4rzGFhD5Ka4cbkjHwfwOf9EkXqV8QAemlv1PdqaczbrEcPuBdgD2rIhURwB1LChuug5TQ8jJFvwKt4cie3UWLnfz2dMJjwh5ex3y60arwIkIumSTXYx_W-nJ7KekRPn3dKZ6nUQlYAUukebN6eeEYQYawjdbkPEEoi0YAXmQCz-VyHfpsmzTd9HmRB3hRWY3sGcWPPof5RmgUY9INv3ckdSgf_RR9S-GuWtEuZSte-1RPtuBHYURycWxXEtJgA7KQic0o77h_uf0i-cMfZfIEdVjQ="
API_KEY = "AIzaSyCvB4NysYtrwxpFUaGb4q_t2ofUV7E1LfU"

api_id = 25054644
api_hash = "d9c07f75d488f15cb655049af0fb686a"

# -------------------------------
# Init Clients
# -------------------------------
client = TelegramClient(StringSession(STRING_SESSION), api_id, api_hash)
gemini_client = genai.Client(api_key=API_KEY)

# Folder untuk menyimpan website user
os.makedirs("websites", exist_ok=True)

# -------------------------------
# Helper Functions
# -------------------------------
async def create_website_files(prompt, theme="default"):
    """Generate website using Gemini AI and save as files"""
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Buatkan website HTML lengkap dengan tema {theme} berdasarkan ide berikut: {prompt}"
    )

    website_content = response.text
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_path = f"websites/{prompt}_{timestamp}"
    os.makedirs(folder_path, exist_ok=True)

    # Buat file index.html
    html_path = os.path.join(folder_path, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(website_content)

    # Bisa buat dummy style.css & script.js, user bisa update nanti
    css_path = os.path.join(folder_path, "style.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write("/* Add your CSS here */\nbody { font-family: Arial; }")

    js_path = os.path.join(folder_path, "script.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Add your JS here\nconsole.log('Website loaded');")

    # Buat zip
    zip_path = os.path.join(folder_path, f"{prompt}_{timestamp}.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(html_path, "index.html")
        zipf.write(css_path, "style.css")
        zipf.write(js_path, "script.js")

    return folder_path, zip_path, website_content

# -------------------------------
# Commands
# -------------------------------
@client.on(events.NewMessage(pattern="/help"))
async def help_cmd(event):
    help_text = (
        "/createweb [ide] - Buat website baru\n"
        "/preview [ide] - Preview website\n"
        "/downloadweb [ide] - Download file zip\n"
        "/updateweb [ide] - Update website\n"
        "/theme [tema] - Ganti tema website\n"
        "/help - Tampilkan perintah\n"
    )
    await event.reply(help_text)

@client.on(events.NewMessage(pattern="/createweb"))
async def create_web(event):
    try:
        user_input = event.message.text.split(" ", 1)[1]
        msg = await event.reply(f"Sedang membuat website '{user_input}'... ⏳")

        folder, zip_file, html_content = await create_website_files(user_input)

        # Update user tentang progress
        for i in range(3):
            await asyncio.sleep(1)
            await msg.edit(f"Sedang membuat website '{user_input}'... {'.'* (i+1)}")

        await msg.edit(f"Website '{user_input}' berhasil dibuat! ✅\nKamu bisa download dengan /downloadweb {user_input}")

    except IndexError:
        await event.reply("Gunakan format: /createweb [ide website]")
    except Exception as e:
        await event.reply(f"Terjadi error: {e}")

@client.on(events.NewMessage(pattern="/preview"))
async def preview_web(event):
    try:
        prompt = event.message.text.split(" ", 1)[1]
        folder = [f for f in os.listdir("websites") if f.startswith(prompt)]
        if not folder:
            await event.reply("Website tidak ditemukan. Buat dulu dengan /createweb")
            return
        folder_path = os.path.join("websites", folder[-1])
        html_file = os.path.join(folder_path, "index.html")
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        # Kirim preview sebagai text
        await event.reply(f"Preview '{prompt}':\n\n{html_content[:1000]}...")  # Limit text
    except Exception as e:
        await event.reply(f"Terjadi error: {e}")

@client.on(events.NewMessage(pattern="/downloadweb"))
async def download_web(event):
    try:
        prompt = event.message.text.split(" ", 1)[1]
        folder = [f for f in os.listdir("websites") if f.startswith(prompt)]
        if not folder:
            await event.reply("Website tidak ditemukan. Buat dulu dengan /createweb")
            return
        folder_path = os.path.join("websites", folder[-1])
        zip_file = [f for f in os.listdir(folder_path) if f.endswith(".zip")][0]
        zip_path = os.path.join(folder_path, zip_file)
        await event.reply(file=zip_path)
    except Exception as e:
        await event.reply(f"Terjadi error: {e}")

@client.on(events.NewMessage(pattern="/theme"))
async def theme_web(event):
    try:
        parts = event.message.text.split(" ", 1)
        if len(parts) < 2:
            await event.reply("Gunakan format: /theme [tema]")
            return
        theme_name = parts[1]
        await event.reply(f"Tema website diubah menjadi '{theme_name}'")
    except Exception as e:
        await event.reply(f"Terjadi error: {e}")

# -------------------------------
# Start Client
# -------------------------------
print("Userbot Telegram siap digunakan...")
client.start()
client.run_until_disconnected()
