from telethon import TelegramClient, events
from telethon.sessions import StringSession
from google import genai
# STRING_SESSION Telegram kamu
STRING_SESSION = "1BVtsOJYBu6Q_ffxWIB4ryDewg6rZ7BREPxvd54Cvu6j2naSg7TZ4C2Vc-UDTCH3_fiES3j4rzGFhD5Ka4cbkjHwfwOf9EkXqV8QAemlv1PdqaczbrEcPuBdgD2rIhURwB1LChuug5TQ8jJFvwKt4cie3UWLnfz2dMJjwh5ex3y60arwIkIumSTXYx_W-nJ7KekRPn3dKZ6nUQlYAUukebN6eeEYQYawjdbkPEEoi0YAXmQCz-VyHfpsmzTd9HmRB3hRWY3sGcWPPof5RmgUY9INv3ckdSgf_RR9S-GuWtEuZSte-1RPtuBHYURycWxXEtJgA7KQic0o77h_uf0i-cMfZfIEdVjQ="

# API Key Gemini AI
os.environ["GENAI_API_KEY"] = "AIzaSyCvB4NysYtrwxpFUaGb4q_t2ofUV7E1LfU"

# Inisialisasi client Gemini
gemini_client = genai.Client()

# Telegram API ID & Hash (ganti dengan milikmu dari my.telegram.org)
api_id = 25054644
api_hash = "d9c07f75d488f15cb655049af0fb686a"

# Inisialisasi Telegram Client
client = TelegramClient(StringSession(STRING_SESSION), api_id, api_hash)

@client.on(events.NewMessage(pattern='/createweb'))
async def create_web(event):
    try:
        # Ambil prompt dari user
        user_input = event.message.text.split(' ', 1)[1]
        await event.reply("Sedang membuat website menggunakan Gemini AI... 🌐")

        # Generate konten website menggunakan Gemini AI
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Buatkan website HTML lengkap berdasarkan ide berikut: {user_input}"
        )

        website_html = response.text

        # Simpan ke file sementara
        file_name = "website.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(website_html)

        # Kirim file HTML ke Telegram
        await event.reply(file=website_html)
        await event.reply(f"Website berhasil dibuat! Kamu bisa download filenya: {file_name}")

    except IndexError:
        await event.reply("Gunakan format: /createweb [ide website]")
    except Exception as e:
        await event.reply(f"Terjadi error: {e}")

print("Userbot Telegram siap digunakan...")
client.start()
client.run_until_disconnected()
