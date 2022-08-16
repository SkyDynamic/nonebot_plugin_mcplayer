import json,os
from .Main import *
from nonebot.plugin import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import GROUP

player = on_command('player',aliases={'获取玩家列表','玩家'},priority=50,permission=GROUP)
bind = on_command("bind", aliases={"绑定"},priority=5,permission=GROUP)
delete = on_command("delete",priority=5,permission=GROUP)

helpmsg = '''----GetServerPlayerPlugin_v1.2.0----
    /bind <服务器IP> <服务器端口(没有则输入0)> <服务器名称> -> 绑定服务器 (等效指令：/绑定)
    /player -> 获取玩家列表 (等效指令：/获取玩家列表，/玩家)
    /player help -> 显示此信息
    /delete -> 删除此群绑定的服务器

    注：由于动空的技术问题，此插件目前不能直接修改绑定后服务器的信息。如果要修改可以将服务器删除后再次添加
    此项目已开源，为免费项目，不允许倒卖，修改等行为。转载请标明作者与出处''' 

default_json = {}

def readjson():
    if not os.path.exists('src/config.json'):
        with open('src/config.json', 'w', encoding='utf-8') as fi:
            json.dump(default_json, fi, ensure_ascii=False, indent=4)
        with open('src/config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open('src/config.json', 'r', encoding='utf-8') as fi:
            return json.load(fi)

@delete.handle()
async def _(event: MessageEvent):
    session = event.get_session_id()
    group_id = session.split('_')[1]
    json_list = readjson()
    json_item = len(json_list)
    for i in range(json_item):
        if group_id == json_list[i]['group_id']:
            del json_list[i]
        with open('src/config.json', 'w', encoding='utf-8') as f:
            json.dump(json_list, f, ensure_ascii=False, indent=4)
    await delete.finish(f"群{group_id}已成功删除服务器")

@player.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    arg1 = str(arg).split(' ')
    tag = arg1[0]
    session = event.get_session_id()
    group_id = session.split('_')[1]
    if not tag:
        await player.send(Main(readjson(), group_id))
    elif tag == 'help':
        await player.send(helpmsg)

@bind.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    session = event.get_session_id()
    group_id = session.split('_')[1]
    arg1 = str(arg).split(' ')
    if len(arg1) == 3:
        IP= arg1[0]
        PORT = arg1[1]
        NAME = arg1[2]
        json_list = readjson()
        if json_list == {}:
            writejson(group_id, IP, PORT, NAME)
            await bind.finish(f"群({group_id})绑定成功!")
        if group_id[group_id]:
            await bind.finish(f"此群({group_id})已经绑定服务器!")
        if group_id != [group_id]:
            writejson(group_id, IP, PORT, NAME)
            await bind.finish(f"群({group_id})绑定成功!")
    else:
        await bind.send('缺少关键信息，绑定失败')

def writejson(group_id, Server_host, Server_port, Server_name):
    if Server_port == '0':
        server_json = {'server_ip': f'{Server_host}','Server_Name': f'{Server_name}'}
    if Server_port != '0':
        server_json = {'server_ip': f'{Server_host}:{Server_port}','Server_Name': f'{Server_name}'}
    alljson = readjson()
    alljson[str(group_id)] = server_json
    with open('src/config.json', 'w', encoding='utf-8') as f1:
        json.dump(alljson, f1, ensure_ascii=False, indent=4)

