import unicodedata
from telethon import TelegramClient, events

API_ID = 23638623
API_HASH = "cf4dc23e593aa80029e654cd3a805912"
GROUP_ID = -1002169348569
BUTTON_TEXT = "Abrir Porton"
SESSION_NAME = "porton_session"

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
    found = False
    async for message in client.iter_messages(GROUP_ID, limit=50):
        if message.buttons:
            for row in message.buttons:
                for btn in row:
                    btn_text = getattr(btn, "text", "")
                    print(f"🔎 Vi botón: {btn_text}")
                    if TARGET in norm(btn_text):
                        await btn.click()  # ✅ cambio aquí
                        await event.reply("✅ Portón abierto")
                        print("✅ Click enviado")
                        found = True
                        return
    if not found:
        await event.reply("❌ No encontré el botón en los últimos mensajes")

client.start()
print("🤖 Bot corriendo... escribe /abrir desde cualquier chat")
client.run_until_disconnected()
