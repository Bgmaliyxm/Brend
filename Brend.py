import os
import importlib
from telethon import events, TelegramClient
import datetime
import requests

# API bilgileri
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'

# Bot ismi
bot_name = 'BrendUserbot'

# TelegramClient nesnesi oluşturuluyor
client = TelegramClient('userbot', api_id, api_hash)

plugin_directory = 'path_to_plugins'
aliases = {}
warns = {}

@client.on(events.NewMessage(pattern=r'\.start|,start|!start'))
async def start(event):
    await event.respond(f'Salam! Mən bir istifadəçi botuyam. Sizi necə kömək edə bilərəm? Sahibim {bot_name} tərəfindən yaradıldım.')

@client.on(events.NewMessage(pattern=r'\.ping|,ping|!ping'))
async def ping(event):
    await event.respond(f'Pong! Sahibim {bot_name} tərəfindən yaradılmışam.')

@client.on(events.NewMessage(pattern=r'\.echo|,echo|!echo'))
async def echo(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        await event.respond(reply_message.text)
    else:
        await event.respond('Xahiş edirəm, cavab verdiyiniz bir mesaja əsaslanaraq istifadə edin.')

@client.on(events.NewMessage(pattern=r'\.upper|,upper|!upper'))
async def upper(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        await event.respond(reply_message.text.upper())
    else:
        await event.respond('Xahiş edirəm, cavab verdiyiniz bir mesaja əsaslanaraq istifadə edin.')

@client.on(events.NewMessage(pattern=r'\.lower|,lower|!lower'))
async def lower(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        await event.respond(reply_message.text.lower())
    else:
        await event.respond('Xahiş edirəm, cavab verdiyiniz bir mesaja əsaslanaraq istifadə edin.')

@client.on(events.NewMessage(pattern=r'\.reverse|,reverse|!reverse'))
async def reverse(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        await event.respond(reply_message.text[::-1])
    else:
        await event.respond('Xahiş edirəm, cavab verdiyiniz bir mesaja əsaslanaraq istifadə edin.')

@client.on(events.NewMessage(pattern=r'\.repeat (\d+)|,repeat (\d+)|!repeat (\d+)'))
async def repeat(event):
    if event.is_reply:
        count = int(event.pattern_match.group(1))
        reply_message = await event.get_reply_message()
        await event.respond(reply_message.text * count)
    else:
        await event.respond('Xahiş edirəm, cavab verdiyiniz bir mesaja əsaslanaraq və təkrar sayınızı qeyd edin.')

@client.on(events.NewMessage(pattern=r'\.time|,time|!time'))
async def time(event):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await event.respond(f'Hal-hazırda tarix və saat: {now}')

@client.on(events.NewMessage(pattern=r'\.sum (\d+) (\d+)|,sum (\d+) (\d+)|!sum (\d+) (\d+)'))
async def sum(event):
    n1 = int(event.pattern_match.group(1))
    n2 = int(event.pattern_match.group(2))
    await event.respond(str(n1 + n2))

@client.on(events.NewMessage(pattern=r'\.sub (\d+) (\d+)|,sub (\d+) (\d+)|!sub (\d+) (\d+)'))
async def sub(event):
    n1 = int(event.pattern_match.group(1))
    n2 = int(event.pattern_match.group(2))
    await event.respond(str(n1 - n2))

@client.on(events.NewMessage(pattern=r'\.mul (\d+) (\d+)|,mul (\d+) (\d+)|!mul (\d+) (\d+)'))
async def mul(event):
    n1 = int(event.pattern_match.group(1))
    n2 = int(event.pattern_match.group(2))
    await event.respond(str(n1 * n2))

@client.on(events.NewMessage(pattern=r'\.div (\d+) (\d+)|,div (\d+) (\d+)|!div (\d+) (\d+)'))
async def div(event):
    n1 = int(event.pattern_match.group(1))
    n2 = int(event.pattern_match.group(2))
    if n2 == 0:
        await event.respond("Sıfıra bölmə xətası!")
    else:
        await event.respond(str(n1 / n2))

@client.on(events.NewMessage(pattern=r'\.weather (.+)|,weather (.+)|!weather (.+)'))
async def weather(event):
    city = event.pattern_match.group(1)
    api_key = 'YOUR_WEATHER_API_KEY'  # Weather API anahtarınızı burada belirtin.
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temperature = data['main']['temp']
        await event.respond(f'Şəhər: {city}\nHava şəraiti: {weather_desc}\nTemperatur: {temperature}°C')
    else:
        await event.respond(f'Şəhər {city} tapılmadı.')

@client.on(events.NewMessage(pattern=r'\.kick (.+)|,kick (.+)|!kick (.+)'))
async def kick(event):
    try:
        user = await event.client.get_entity(event.pattern_match.group(1))
        await event.client.kick_participant(event.chat_id, user.id)
        await event.respond(f'{user.username} istifadəçisi qrupdan çıxarıldı.')
    except Exception as e:
        await event.respond(f'Hata: {str(e)}')

@client.on(events.NewMessage(pattern=r'\.list-groups|,list-groups|!list-groups'))
async def list_groups(event):
    groups = await client.get_dialogs()
    group_list = [dialog.name for dialog in groups if dialog.is_group]
    await event.respond("\n".join(group_list))

@client.on(events.NewMessage(pattern=r'\.mute (.+) (\d+)|,mute (.+) (\d+)|!mute (.+) (\d+)'))
async def mute(event):
    try:
        user = await event.client.get_entity(event.pattern_match.group(1))
        seconds = int(event.pattern_match.group(2))
        await event.client.edit_permissions(event.chat_id, user, until_date=datetime.datetime.now() + datetime.timedelta(seconds=seconds))
        await event.respond(f'{user.username} istifadəçisi {seconds} saniyəlik səssizləşdirildi.')
    except Exception as e:
        await event.respond(f'Hata: {str(e)}')

@client.on(events.NewMessage(pattern=r'\.unmute (.+)|,unmute (.+)|!unmute (.+)'))
async def unmute(event):
    try:
        user = await event.client.get_entity(event.pattern_match.group(1))
        await event.client.edit_permissions(event.chat_id, user, until_date=None)
        await event.respond(f'{user.username} istifadəçisinin səssizləşdirilməsi dayandırıldı.')
    except Exception as e:
        await event.respond(f'Hata: {str(e)}')

@client.on(events.NewMessage(pattern=r'\.set-alias (.+) (.+)|,set-alias (.+) (.+)|!set-alias (.+) (.+)'))
async def set_alias(event):
    try:
        username = event.pattern_match.group(1)
        alias = event.pattern_match.group(2)
        aliases[username] = alias
        await event.respond(f'{username} istifadəçisinə "{alias}" olaraq təyinat verildi.')
    except Exception as e:
        await event.respond(f'Hata: {str(e)}')

@client.on(events.NewMessage(pattern=r'\.get-alias (.+)|,get-alias (.+)|!get-alias (.+)'))
async def get_alias(event):
    try:
        username = event.pattern_match.group(1)
        alias = aliases.get(username, "Tapılmadı.")
        await event.respond(f'{username} istifadəçisinə verilən təyinat: {alias}')
    except Exception as e:
        await event.respond(f'Hata: {str(e)}')

@client.on(events.NewMessage(pattern=r'\.warn (.+) (.+)|,warn (.+) (.+)|!warn (.+) (.+)'))
async def warn(event):
    try:
        user = await event.client.get_entity(event.pattern_match.group(1))
        reason = event.pattern_match.group(2)
        if user.id not in warns:
            warns[user.id] = []
        warns[user.id].append(reason)
        await event.respond(f'{user.username} istifadəçisinə "{reason}" səbəbindən xəbərdarlıq göndərildi.')
    except Exception as e:
        await event.respond(f'Hata: {str(e)}')

@client.on(events.NewMessage(pattern=r'\.unwarn (.+)|,unwarn (.+)|!unwarn (.+)'))
async def unwarn(event):
    try:
        user = await event.client.get_entity
