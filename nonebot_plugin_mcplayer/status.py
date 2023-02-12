from mcstatus import JavaServer
from .config import Config

config = Config()

class Get_Status:
    def __init__(self, group_id: str):
        self.group_id = group_id

    async def Status(self):
        data = config.read()
        if self.group_id not in data:
            self.status = f'Error: 此群未绑定服务器'
        else:
            try:
                ip = f'''{data[self.group_id]['ip']}{f':{data[self.group_id]["port"]}' if data[self.group_id]['port'] != 25565 else ''}'''
                server = JavaServer.lookup(ip)
                status = server.status()
                player_list = []
                for p in status.players.sample:
                    player_list.append(p.name)
                self.status = 'OK'
                self.server_name = data[self.group_id]['name']
                self.max_player = status.players.max
                self.online_player = status.players.online
                self.player_list = player_list
            except Exception as e:
                self.status = f'Error: {e}'