`import json,os

from mcstatus import JavaServer
from nonebot.plugin import on_keyword,on_command
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message

player_list = []
player = on_keyword(['player','获取玩家列表','玩家'],priority=50)
bind = on_command("bind", aliases={"绑定"}, priority=5)
delete = on_keyword(["delete","删除服务器","删除","del"],priority=5)
sendhelp = on_keyword(["help","帮助"],priority=5)

@sendhelp.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    helpmsg = '''----GetServerPlayerPlugin_v1.0.0----
    /help -> 显示这条信息 (等效指令:/帮助)
    /bind -> 绑定服务器 (等效指令：/绑定)(输入后请按机器人提示输入信息哦)
    /player -> 获取玩家列表 (等效指令：/获取玩家列表，/玩家)
    /delete -> 删除此群绑定的服务器 (等效指令：/删除服务器，/删除，/del)

    注：由于动空的技术问题，此插件目前不能直接修改绑定后服务器的信息。如果要修改可以将服务器删除后再次添加
    此项目已开源，为免费项目，不允许倒卖，修改等行为。转载请标明作者与出处''' 
    await sendhelp.send(Message(helpmsg))

@player.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    global player_list
    session = event.get_session_id()
    group_id = session.split('_')[1]
    message = main(group_id)
    player_list = []
    await player.send(Message(message))

@bind.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("server", args)

@delete.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    session = event.get_session_id()
    group_id = session.split('_')[1]
    json_list = readjson()
    json_item = len(json_list)
    for i in range(json_item):
        if group_id == json_list[i]['group_id']:
            del json_list[i]
        with open('player/config.json', 'w', encoding='utf-8') as f:
            json.dump(json_list, f, ensure_ascii=False, indent=4)
    await delete.finish(f"群{group_id}已成功删除服务器")

@bind.got('server', prompt="请按以下格式填写服务器信息：服务器地址!服务器端口!服务器名字（!是分界线，必填！如果没有端口，请在服务器断口处填上0！）")
async def handle_server( event: Event, server: Message = Arg(), server_message: str = ArgPlainText("server")):
    session = event.get_session_id()
    group_id = session.split('_')[1]
    server_msg = server_message.split('!')
    server_name = server_msg[2]
    server_port = server_msg[1]
    server_host = server_msg[0]
    if os.path.exists('player/config.json'):
        json_list = readjson()
        if json_list == []:
            writejson('after', group_id, server_host, server_port, server_name)
            await bind.finish(f"群({group_id})绑定成功!")
        num_json = len(json_list)
        for i in range(num_json):
            if group_id == json_list[i]['group_id']:
                await bind.finish(f"此群({group_id})已经绑定服务器!")
            if group_id != json_list[i]['group_id']:
                writejson('after', group_id, server_host, server_port, server_name)
                await bind.finish(f"群({group_id})绑定成功!")
    if not os.path.exists('player/config.json'):
        writejson('first', group_id, server_host, server_port, server_name)
        await bind.finish(f"群({group_id})绑定成功！")

def readjson():
    if not os.path.exists('player/config.json'):
        return False
    else:
        with open('player/config.json', 'r', encoding='utf-8') as fi:
            return json.load(fi)

def writejson(mode, group_id, Server_host, Server_port, Server_name):
    if Server_port == '0':
        server_json = {'group_id': f'{group_id}','server_ip': f'{Server_host}','Server_Name': f'{Server_name}'}
        first_json = [{'group_id': f'{group_id}','server_ip': f'{Server_host}','Server_Name': f'{Server_name}'}]
    if Server_port != '0':
        server_json = {'group_id': f'{group_id}','server_ip': f'{Server_host}:{Server_port}','Server_Name': f'{Server_name}'}
        first_json = [{'group_id': f'{group_id}','server_ip': f'{Server_host}:{Server_port}','Server_Name': f'{Server_name}'}]
    if mode == 'first':
        with open('player/config.json', 'w', encoding='utf-8') as f:
            json.dump(first_json, f, ensure_ascii=False, indent=4)
    if mode == 'after':
        item_list = []
        alljson = readjson()
        num_item = len(alljson)
        for i in range(num_item):
            group = alljson[i]['group_id']
            server_ip = alljson[i]['server_ip']
            Server_Name = alljson[i]['Server_Name']
            item_dict = {'group_id': f'{group}','server_ip': f'{server_ip}','Server_Name': f'{Server_Name}'}
            item_list.append(item_dict)
        item_list.append(server_json)
        with open('player/config.json', 'w', encoding='utf-8') as f1:
            json.dump(item_list, f1, ensure_ascii=False, indent=4)

def main(group_id):
    json = readjson()
    if json == [] or json == False:
        return '此群未绑定服务器！'
    if json != []:
        json_num = len(json)
        for i in range(json_num):
            if json[i]['group_id'] == group_id:
                server_ip = json[i]['server_ip']
                server_name = json[i]['Server_Name']
            server = JavaServer.lookup(server_ip)
            status = server.status()
            for p in status.players.sample:
                player_list.append(p.name)
            message = f'------{server_name}当前状态------\n' + f'最大人数：{str(status.players.max)}\n' + f'当前在线人数：{str(status.players.online)}\n' + '当前在线玩家：\n- ' + '\n- '.join(player_list)
            if group_id not in json[i]['group_id']:
                message == '此群未绑定服务器！'
            return message
