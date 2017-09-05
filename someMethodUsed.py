import socket
import os
import subprocess

# 获取本地无线iP
def getIp():
    local_ip = socket.gethostbyname(socket.gethostname())

    print("getByHostName:",local_ip,",hostName:",socket.gethostname())

    ip_list = socket.gethostbyname_ex(socket.gethostname())
    addr_ip = socket.gethostbyaddr(socket.gethostname())
    print("getHostByAddr:",addr_ip)
    for ip in ip_list:
        print("ip:",ip)


# 判断有没有连上网络,通过Ping命令来判断
def canConnect():
    fnull = open(os.devnull,'w')
    result = subprocess.call('ping www.baidu.com',shell=True,stdout=fnull,stderr=fnull)
    fnull.close()
    print("result:",result)
    if result:#返回非0则连接失败
        return False
    else:
        return True
    # return os.system('ping www.baidu.com')

if __name__ == '__main__':
    getIp()
    print("canConnect:",canConnect())
