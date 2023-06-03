import requests
from vultr import Vultr
import re
import time
import json
import random

vultr = Vultr(api_key="xxxxx")#APIKEY

#创建服务器（大约需要四~五分钟）
def createserver():
    server = vultr.server.create(
        dcid=random.randint(1,30),  # Datacenter ID，随机国家的选择
        vpsplanid=480,  # VPS Plan ID 固定选择什么类型和配置的服务器，这里我选的是最便宜的
        osid=1946,  # Operating System ID
    )
    time.sleep(40)#等待创建time，vultr的缺点，或者说几大知名服务器的缺点就是创建和释放的服务器特别慢
    SUBID = int(server['SUBID'])
    print(f"新的服务器的subid: {SUBID}")

    new_servers = vultr.server.list(subid=SUBID)  # 获取服务器信息列表

    str_servers = str(new_servers)  # 转成字符串的形式
    ip = re.search(r"'main_ip': '(.*?)', 'vcp", str_servers)  # 远程连接服务器IP，只获取ip
    ip = ip.group(1)

    return ip,SUBID

def breakserver(SUBID):
    SUBID2=int(SUBID)
    vultr.server.destroy(SUBID2)  # 删除当前服务器
    print(f"{SUBID}:删除成功！\n")
    #time.sleep(5)

sourse="Vultr"

# POST请求


for i in range(0, 15):#循环创建15次
    try:
        ip1, SUBID1 = createserver()  # 创建服务器并返回ip和SUBID
        print(ip1,SUBID1)
    except:
        print("创建失败，跳过！")
        continue

    while True:
        try:
            breakserver(SUBID1)
        except:
            print("诶呀删不掉，等60s再试一次！")
            time.sleep(60)
