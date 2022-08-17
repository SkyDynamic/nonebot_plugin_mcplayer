from mcstatus import JavaServer
from mcstatus.address import Address
from mcstatus.pinger import ServerPinger
from mcstatus.protocol.connection import TCPSocketConnection

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
            server = JavaServer.lookup(server_ip[0])
            try:
                status = server.status()
                for p in status.players.sample:
                    player_list.append(p.name)
                message = f'------{server_name}当前状态------\n' + f'最大人数：{str(status.players.max)}\n' + f'当前在线人数：{str(status.players.online)}\n' + '当前在线玩家：\n- ' + '\n- '.join(player_list)
            except TypeError as e:
                message = f'------{server_name}当前状态------\n' + f'最大人数：{str(status.players.max)}\n' + f'当前在线人数：0\n' + '当前在线玩家：\n\n--没有玩家在线--'
            except TimeoutError as e2:
                message = '[TimeOutError]服务器连接超时，请稍后再试。如仍然无法连接请检查服务器是否能正常连接并联系机器人管理员'
            except ConnectionRefusedError as e3:
                message = '[ConnectionRefusedError]服务器是否未开启或无法连接'
            except OSError as e1:
                message = self.second_try(self,server_ip, server_name)
            return message

    def second_try(self, ip, server_name):
        server_ip = str(ip).split(':')
        if len(server_ip) == 2:
            address = Address(server_ip[0], int(server_ip[1]))
        elif len(server_ip) == 1:
            address = Address(server_ip[0], 25565)
        try:
            pinger = ServerPinger(TCPSocketConnection(address, timeout=5), address=address)
            pinger.handshake()
            status = pinger.read_status()
            for p in status.players.sample:
                player_list.append(p.name)
            message = f'------{server_name}当前状态------\n' + f'最大人数：{str(status.players.max)}\n' + f'当前在线人数：{str(status.players.online)}\n' + '当前在线玩家：\n- ' + '\n- '.join(player_list)
        except TypeError as e:
            message = f'------{server_name}当前状态------\n' + f'最大人数：{str(status.players.max)}\n' + f'当前在线人数：0\n' + '当前在线玩家：\n\n--没有玩家在线--'
        except ConnectionRefusedError as e3:
            message = '[ConnectionRefusedError]服务器是否未开启或无法连接'
        except TimeoutError as e2:
            message = '[TimeOutError]服务器连接超时，请稍后再试。如仍然无法连接请检查服务器是否能正常连接并联系机器人管理员'
        return message
