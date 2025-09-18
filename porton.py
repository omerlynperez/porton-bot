import os
import unicodedata
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
GROUP_ID = int(os.getenv("GROUP_ID"))
CONTROL_CHAT_ID = int(os.getenv("CONTROL_CHAT_ID"))
BUTTON_TEXT = os.getenv("BUTTON_TEXT", "Abrir Porton")
SESSION_NAME = os.getenv("SESSION_NAME", "porton_session")

def norm(s: str) -> str:
    if not s: 
        return ""
    s = s.lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    for ch in "()[]{}-_ .·•":
        s = s.replace(ch, "")
    return s

TARGET = norm(BUTTON_TEXT)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r"^/abrir$"))
async def on_cmd(event):
    print(f"📩 Recibí comando desde chat {event.chat_id}")
    # Aceptar desde cualquier chat (si quieres limitar, compara con CONTROL_CHAT_ID)
    found = False
    async for message in client.iter_messages(GROUP_ID, limit=50):
        if message.buttons:
            for row in message.buttons:
                for btn in row:
                    btn_text = getattr(btn, "text", "")
                    print(f"🔎 Vi botón: {btn_text}")
                    if TARGET in norm(btn_text):
                        await message.click(btn)
                        await event.reply("✅ Portón abierto")
                        print("✅ Click enviado")
                        found = True
                        return
    if not found:
        await event.reply("❌ No encontré el botón en los últimos mensajes")

client.start()
print("🤖 Bot corriendo en Railway... escribe /abrir en tu chat de control")
client.run_until_disconnected()


