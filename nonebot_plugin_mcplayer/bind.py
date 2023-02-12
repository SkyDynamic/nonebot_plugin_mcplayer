from .config import Config

class Bind:
    def __init__(self, group_id: str, server_name: str, server_ip: str, server_port: int = 25565):
        config = Config()
        data = config.read()
        data[group_id] = {
            'name': server_name,
            'ip': server_ip,
            'port': server_port
        }
        config.write(data)

class Delete:
    def __init__(self, group_id: str):
        config = Config()
        data = config.read()
        if group_id in data:
            del data[group_id]
            config.write(data)
            self.result = '删除成功'
        else:
            self.result = 'Error: 此群未绑定服务器'