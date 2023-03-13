from utils import rds
import requests
from utils.config import Config


def ipport2url(ip : str, port : int) -> str:
    return 'http://' + ip + ':' + str(port) + '/api'

def suffix2url(suffix : str) -> str:
    dic = requests.get(Config.config_service_ip + f'/{suffix}').json()
    return ipport2url(dic['ip'], dic['port'])

manager_url = suffix2url('manager')
scaler_url = suffix2url('scaler')

lis = requests.get(Config.config_service_ip + '/memcache').json()["cache_config_list"]

memcache_url = [ipport2url(dic['ip'], dic['port']) for dic in lis]

def id2url(id : int) -> str:
    return memcache_url[id]


