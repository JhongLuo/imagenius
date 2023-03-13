import requests
import paramiko
import time

rds_config = {
    "user" : "root",
    "password" : "ece1779pass",
    "host" : "biggerdb.cvtl8zx5dggi.us-east-1.rds.amazonaws.com",
    "database" : "ece1779a2",
}

manager_config = {
    "ip" : "54.146.182.23",
    "port" : 5000,
}

scaler_config = {
    "ip" : "18.212.9.246",
    "port" : 5002,
}

memcache_config = [
{
    "ip" : "34.227.61.73",
    "port" : 5000,
},
{
    "ip" : "52.2.163.58",
    "port" : 5000,
},
{
    "ip" : "54.147.48.130",
    "port" : 5000,
},
{
    "ip" : "54.90.119.128",
    "port" : 5000,
},
{
    "ip" : "54.226.203.158",
    "port" : 5000,
},
{
    "ip" : "34.230.75.249",
    "port" : 5000,
},
{
    "ip" : "52.91.242.195",
    "port" : 5000,
},
{
    "ip" : "52.87.176.18",
    "port" : 5000,
}]


def ssh_connect(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    ssh.connect(hostname=ip, username="ubuntu", key_filename='/Users/jhong/Downloads/jhong.pem')
    return ssh

def kill(ssh, port):
    _, out, _ = ssh.exec_command('sudo kill -9 $(sudo lsof -t -i :{})'.format(port))
    out.channel.recv_exit_status()
    print(out.readlines())

def python_run(ssh, filepath, para = ''):
    _, out, _ = ssh.exec_command(f'nohup python3 {filepath} {para} > output.log 2>&1 &')
    out.channel.recv_exit_status()
    print(out.readlines())
    time.sleep(2)

def run_config_server():
    config_server_ip = "44.205.186.249"
    ssh = ssh_connect(config_server_ip)
    kill(ssh, 5201)
    python_run(ssh, "personal-service-flask/server/run.py")
    ssh.close()
    print("config server is running")

backend_path = "images-sharing-website/a2-backend/"

def set_config_server():       
    config_server_url = "http://44.205.186.249:5201/api/ece1779/a2/config/"
    print(requests.post(config_server_url + "rds", json = rds_config).json())
    print(requests.post(config_server_url + "manager", json = manager_config).json())
    print(requests.post(config_server_url + "scaler", json = scaler_config).json())
    print(requests.post(config_server_url + "memcache", json = {"cache_config_list" : memcache_config}).json())
    

def run_memcache():
    for i, dic in enumerate(memcache_config):
        ip = dic["ip"]
        port = dic["port"]
        ssh = ssh_connect(ip)
        kill(ssh, port)
        python_run(ssh, backend_path + "run_memcache.py", port)
        ssh.close()
        print(f"memcache server {i} is running")

def run_auto_scaler():
    ip = scaler_config["ip"]
    port = scaler_config["port"]
    ssh = ssh_connect(ip)
    kill(ssh, port)
    python_run(ssh, backend_path + "run_auto_scaler.py")
    ssh.close()
    print("auto scaler is running")
    
def run_manager():
    ip = manager_config["ip"]
    port = manager_config["port"]
    ssh = ssh_connect(ip)
    kill(ssh, port)
    python_run(ssh, backend_path + "run_manager.py")
    ssh.close()
    print("manager is running")
    
    
# run_config_server()
# set_config_server()
run_memcache()
run_auto_scaler()
run_manager()
