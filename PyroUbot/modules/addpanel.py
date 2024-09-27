
import os
import json
import aiohttp
import asyncio
import random
import string
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from PyroUbot import PY
from PyroUbot.config import OWNER_ID, PLTA, DOMAIN, CAPI_KEY, EGG, LOC

__MODULE__ = "ᴘᴛᴇʀᴏᴅᴀᴄᴛʏʟ"
__HELP__ = """
<blockquote><b>Contoh menggunakan fitur Panel Management</b>
  <b>• Perintah:</b> .addadmin namapanel idtele
  <b>• Penjelasan:</b> Untuk menambahkan admin panel baru
  
  <b>• Perintah:</b> .delpanel idserver
  <b>• Penjelasan:</b> Untuk menghapus admin panel
  
  <b>• Perintah:</b> .addpanel Username Ram
  <b>• Penjelasan:</b> Untuk menambahkan panel
  
  <b>• Perintah:</b> .listadmin
  <b>• Penjelasan:</b> Untuk Memunculkan List Admin

  <b>• Perintah:</b> .listpanel
  <b>• Penjelasan:</b> Untuk Memunculkan List Panel Server

  <b>• Note:</b> Hanya dapat digunakan oleh owner</blockquote>
"""

def escape_markdown(text):
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    return ''.join('\\' + char if char in escape_chars else char for char in str(text))

async def is_owner(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply_text("Maaf, hanya owner yang dapat menggunakan perintah ini.")
        return False
    return True

@PY.UBOT("addadmin|cadmin")
async def add_admin_command(client: Client, message: Message):
    if not await is_owner(client, message):
        return

    try:
        command_params = message.text.split()[1:]
        panel_name = command_params[0]
        telegram_id = command_params[1]
    except IndexError:
        await message.reply_text("""<blockquote><emoji id=5032973497861669622>❌</emoji>[ ғᴏʀᴍᴀᴛ ᴠᴀʟɪᴅ ] ᴄᴏɴᴛᴏʜ : .ᴀᴅᴅᴀᴅᴍɪɴ ᴜsᴇʀɴᴀᴍᴇ ɪᴅᴛᴇʟᴇɢʀᴀᴍ</blockquote>
<blockquote><emoji id=6008220984346152956>📣</emoji>SEWA USERBOT 20K/BULAN @Fahrioffic</blockquote>""")
        return

    password = f"{panel_name}117"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{DOMAIN}/api/application/users',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {PLTA}'
            },
            json={
                'email': f'{panel_name}@gmail.com',
                'username': panel_name,
                'first_name': panel_name,
                'last_name': "Memb",
                'language': "en",
                'root_admin': True,
                'password': password
            }
        ) as response:
            data = await response.json()

    if 'errors' in data:
        await message.reply_text(json.dumps(data['errors'][0], indent=2))
        return

    user = data['attributes']
    user_info = f"""
<blockquote>TYPE: ADMIN PANEL
➟ ID: {user['id']}
➟ USERNAME: {user['username']}
➟ EMAIL: {user['email']}
➟ NAME: {user['first_name']} {user['last_name']}
➟ LANGUAGE: {user['language']}
➟ ADMIN: {user['root_admin']}
➟ CREATED AT: {user['created_at']}
➟ LOGIN: <b><a href='{DOMAIN}'>LINK PANEL</a></b></blockquote>
    """
    await message.reply_text(user_info)

    admin_info = f"""
BERIKUT DETAIL AKUN ADMIN PANEL ANDA
HERE'S YOUR ADMIN PANEL DATA ⤵️
🚩 Login : {DOMAIN}
🚩 Username : {panel_name}
🚩 Password : {password}
==============================
<blockquote>➡️ Rules : 
• Jangan Curi Sc
• Jangan Buka Panel Orang
• Jangan Ddos Server
• Kalo jualan sensor domainnya
• Jangan Bagi² Panel Free
• Jangan Jualan AdminP Kecuali Pt Gw !!
NGEYEL? KICK NO REFF NO DRAMA
Jangan Lupa Bilang Done Jika Sudah Di Cek
==============================
THANKS FOR BUYING AT FAHRI - OFFC😁✌️</blockquote>
    """
    await client.send_message(chat_id=telegram_id, text=admin_info)

@PY.UBOT("delpanel")
async def delete_admin_command(client: Client, message: Message):
    if not await is_owner(client, message):
        return

    try:
        server_id = message.text.split()[1]
    except IndexError:
        await message.reply_text('Format Salah! Penggunaan: .deladmin idserver')
        return

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PLTA}"
    }
    
    async with aiohttp.ClientSession() as session:
        # Menghapus server
        async with session.delete(f"{DOMAIN}/api/application/servers/{server_id}", headers=headers) as server_response:
            if not server_response.ok:
                await message.reply_text(f"Gagal menghapus server: {await server_response.json()}")
                return

        # Mengambil daftar pengguna
        async with session.get(f"{DOMAIN}/api/application/users?page=1", headers=headers) as user_response:
            users = (await user_response.json())['data']
    
    deleted_user = None
    for user in users:
        u = user['attributes']
        if u['username'].lower() == server_id.lower():
            # Menghapus pengguna
            async with session.delete(f"{DOMAIN}/api/application/users/{u['id']}", headers=headers) as delete_user_response:
                if not delete_user_response.ok:
                    await message.reply_text(f"Gagal menghapus pengguna: {await delete_user_response.json()}")
                    return
            deleted_user = u['username']
            break
    
    if not deleted_user:
        await message.reply_text("*ID Server/User* tidak ditemukan")
    else:
        await message.reply_text(f"Berhasil menghapus akun panel *{deleted_user.capitalize()}*")
        
@PY.UBOT("addpanel")
async def addpanel_command(client: Client, message: Message):

    if not PLTA:
        await message.reply_text("API key not found!")
        return

    args = message.text.split()[1:]
    if len(args) < 2:
        await message.reply_text("""<blockquote><emoji id=5032973497861669622>❌</emoji>[ ғᴏʀᴍᴀᴛ ᴠᴀʟɪᴅ ] ᴄᴏɴᴛᴏʜ : .ᴀᴅᴅᴘᴀɴᴇʟ ᴜsᴇʀɴᴀᴍᴇ ʀᴀᴍ</blockquote>
<blockquote><emoji id=6008220984346152956>📣</emoji>SEWA USERBOT 20K/BULAN @Fahrioffic</blockquote>""")
        return

    username = args[0].lower()
    ram_option = args[1].lower()

    if username.isdigit():
        await message.reply_text("""<blockquote><emoji id=5032973497861669622>❌</emoji>[ ғᴏʀᴍᴀᴛ ᴠᴀʟɪᴅ ] ᴄᴏɴᴛᴏʜ : .ᴀᴅᴅᴘᴀɴᴇʟ ᴜsᴇʀɴᴀᴍᴇ ʀᴀᴍ</blockquote>
<blockquote><emoji id=6008220984346152956>📣</emoji>SEWA USERBOT 20K/BULAN @Fahrioffic</blockquote>""")
        return

    ram_options = {
        "1gb": ("30", "1000", "1000"),
        "2gb": ("40", "2000", "2000"),
        "3gb": ("50", "3000", "2000"),
        "4gb": ("60", "4000", "2000"),
        "5gb": ("70", "5000", "2000"),
        "6gb": ("80", "6000", "3000"),
        "7gb": ("90", "7000", "3000"),
        "8gb": ("100", "8000", "3000"),
        "9gb": ("110", "9000", "3000"),
        "10gb": ("120", "10000", "4000"),
        "11gb": ("140", "11000", "5000"),
        "12gb": ("150", "12000", "5000"),
        "unli": ("0", "0", "0"),
        "unlimited": ("0", "0", "0")
    }

    if ram_option not in ram_options:
        await message.reply_text("Invalid RAM option!")
        return

    cpu, ram, disk = ram_options[ram_option]

    email = f"{username}@gmail.com"
    name = username.capitalize()
    password = username + ''.join(random.choices(string.hexdigits, k=4))

    async with aiohttp.ClientSession() as session:
        try:
            # Create user
            async with session.post(f"{DOMAIN}/api/application/users", headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {PLTA}"
            }, json={
                "email": email,
                "username": username,
                "first_name": name,
                "last_name": "Server",
                "language": "en",
                "password": password
            }) as response:
                data = await response.json()
                if "errors" in data:
                    await message.reply_text(f"Error: {data['errors'][0]['detail']}")
                    return
                user = data["attributes"]

            # Get egg details
            async with session.get(f"{DOMAIN}/api/application/nests/5/eggs/{EGG}", headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {PLTA}"
            }) as response:
                data2 = await response.json()
                startup_cmd = data2["attributes"]["startup"]

            # Create server
            async with session.post(f"{DOMAIN}/api/application/servers", headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {PLTA}"
            }, json={
                "name": name,
                "description": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": user["id"],
                "egg": int(EGG),
                "docker_image": "ghcr.io/parkervcp/yolks:nodejs_18",
                "startup": startup_cmd,
                "environment": {
                    "INST": "npm",
                    "USER_UPLOAD": "0",
                    "AUTO_UPDATE": "0",
                    "CMD_RUN": "npm start"
                },
                "limits": {
                    "memory": int(ram),
                    "swap": 0,
                    "disk": int(disk),
                    "io": 500,
                    "cpu": int(cpu)
                },
                "feature_limits": {
                    "databases": 5,
                    "backups": 5,
                    "allocations": 5
                },
                "deploy": {
                    "locations": [int(LOC)],
                    "dedicated_ip": False,
                    "port_range": []
                }
            }) as response:
                result = await response.json()
                if "errors" in result:
                    await message.reply_text(f"Error: {result['errors'][0]['detail']}")
                    return
                server = result["attributes"]

            ram_display = "Unlimited" if ram == "0" else f"{int(ram)//1024}GB"
            cpu_display = "Unlimited" if cpu == "0" else f"{cpu}%"
            disk_display = f"{int(disk)//1024}GB"

            response_text = f"""
<emoji id=6008220984346152956>📣</emoji>Successfully Created Panel Account <emoji id=5929274653607465396>☑️</emoji>
• ID: {user['id']}
• Username: {user['username']}
• Password: {password}

<blockquote>YOUR PANEL DETAILS
• RAM: {ram_display}
• CPU: {cpu_display}
• Storage: {disk_display}
• Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
• Login Link ⬇️
<b><a href='{DOMAIN}'>Click Link Login</a></b></blockquote>

NOTE LARANGAN PANEL
<blockquote>• Don't Use For Running DDoS Bots
• Forbidden to Spread Panel Domain
• Strictly Prohibited to Run Heavy Scripts
• All Transactions No Refund</blockquote>
"""
            await message.reply_text(response_text)

        except aiohttp.ClientError as e:
            await message.reply_text(f"An error occurred while communicating with the server: {str(e)}")
        except Exception as e:
            await message.reply_text(f"An unexpected error occurred: {str(e)}")
