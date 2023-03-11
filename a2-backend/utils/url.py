from utils.config import Config

def get_url(ip, port):
    return 'http://' + ip + ':' + str(port) + '/api'

def id2url(id : int) -> str:
    return get_url(*Config.memcache_ip[id])

scaler_url = get_url(*Config.scaler_ip)

manager_url = get_url(*Config.manager_ip)