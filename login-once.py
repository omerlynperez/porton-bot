from telethon.sync import TelegramClient
from getpass import getpass

# Pedimos tus credenciales para iniciar sesión
api_id = int(input("API_ID: "))
api_hash = input("API_HASH: ")
phone = input("Phone (+584XXXXXXXXX): ")

# Creamos la sesión
client = TelegramClient("porton_session", api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    # Enviamos el código de verificación a tu Telegram
    client.send_code_request(phone)
    code = input("Código recibido en Telegram: ")

    try:
        # Intentamos iniciar sesión solo con el código
        client.sign_in(phone=phone, code=code)
    except Exception as e:
        # Si pide la contraseña de verificación en 2 pasos
        if "PasswordNeededError" in str(type(e)):
            password = getpass("Tu contraseña de verificación en 2 pasos: ")
            client.sign_in(password=password)
        else:
            raise e

print("✅ Sesión creada (archivo porton_session.session)")
client.disconnect()
