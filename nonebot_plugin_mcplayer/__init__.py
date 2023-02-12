from nonebot.plugin import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GROUP, GROUP_ADMIN, GROUP_OWNER, Bot, MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from .bind import Bind, Delete
from .status import Get_Status

mcplayer = on_command('mcplayer', priority=0, permission=GROUP)

helpmsg = '''----GetServerPlayerPlugin_v2.0.0----
/mcplayer bind <服务器名称> <服务器IP> <服务器端口(留空则默认25565)> -> 绑定服务器
/mcplayer list -> 获取玩家列表
/mcplayer help -> 显示此信息
/mcplayer delete -> 删除此群绑定的服务器'''

return_msg = '''{0}服务器最大玩家数：{1}
当前在线玩家数：{2}
当前在线玩家列表：
{3}'''

@mcplayer.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    args = str(arg).split()
    reply = MessageSegment.reply(event.message_id)
    if len(args) == 0:
        await mcplayer.finish(reply + helpmsg)
    elif len(args) > 0:

        # 帮助

        if arg[0] == 'help':
            await mcplayer.finish(reply + helpmsg)

        # 绑定处理器(需要群管理员权限)

        if args[0] == 'bind':
            if await GROUP_ADMIN(bot, event) or await GROUP_OWNER(bot, event):
                if len(args) < 3:
                    await mcplayer.finish(reply + '缺少信息')
                elif len(args) >= 3:
                    try:
                        port = args[3]
                    except IndexError as e:
                        port = 25565
                    Bind(str(event.group_id), args[1], args[2], port)
                    await mcplayer.finish(reply + f'''绑定成功,请检查服务器信息:
服务器名称: {args[1]}
服务器IP: {args[2]}
服务器端口: {port}''')
            else:
                await mcplayer.finish(reply + '权限不足')

        # 删除绑定(需要群管理员权限)

        if args[0] == 'delete':
            if await GROUP_ADMIN(bot, event) or await GROUP_OWNER(bot, event):
                result = Delete(str(event.group_id)).result
                await mcplayer.finish(reply + result)
            else:
                await mcplayer.finish(reply + '权限不足')

        # 查询

        if args[0] == 'list':
            status = Get_Status(str(event.group_id))
            await status.Status()
            if status.status == 'OK':
                player_list = ', '.join(status.player_list)
                await mcplayer.finish(return_msg.format(status.server_name, status.max_player, status.online_player, player_list))
            else:
                await mcplayer.finish(reply + status.status)