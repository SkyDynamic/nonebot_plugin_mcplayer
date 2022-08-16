from mcstatus import JavaServer

player_list = []

class Main():
    def __new__(self, json, group_id):
        self.json = json
        self.group_id = group_id
        return self.main(self)

    def main(self):
        if self.json == {} or self.json == False or self.group_id not in self.json:
            return '此群未绑定服务器！'
        if self.json != {}:
            player_list = []
            server_ip = self.json[self.group_id]['server_ip']
            server_name = self.json[self.group_id]['Server_Name']
            server = JavaServer.lookup(server_ip)
            status = server.status()
            try:
                for p in status.players.sample:
                    player_list.append(p.name)
                message = f'------{server_name}当前状态------\n' + f'最大人数：{str(status.players.max)}\n' + f'当前在线人数：{str(status.players.online)}\n' + '当前在线玩家：\n- ' + '\n- '.join(player_list)
            except TypeError as e:
                message = f'------{server_name}当前状态------\n' + f'最大人数：{str(status.players.max)}\n' + f'当前在线人数：0\n' + '当前在线玩家：\n\n--没有玩家在线--'
            return message
