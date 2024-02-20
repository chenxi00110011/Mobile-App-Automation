import logging as log
import re
import socket
import time
from my_decorator import exception_handler ,retry
from scapy.layers.inet import Ether
from scapy.layers.l2 import ARP
from scapy.sendrecv import srp  # scapy 扫描局域网MAC地址

import xrs_time

log.basicConfig(filename=f'C:\\Users\\Administrator\\Desktop\\logs\\{xrs_time.today()}.log', level=log.INFO)


def arp_scan(mac):
    '''
    扫描局域网中的mac，返回符合输入mac的设备ip
    :param mac: 设备的mac，如果输入"ff:ff:ff:ff:ff:ff"，则返回子网中所有的存活设备
    :return: 字典类型，mac、ip映射表
    '''
    mac = str.lower(mac)
    local_ip = socket.gethostbyname(socket.gethostname())
    gateway_ip = re.sub(r'\d+$', '1', local_ip)
    ipscan = f'{gateway_ip}/24'
    arp_table = {}
    try:
        # log.info('dst=',mac,'pdst=',ipscan)
        ans, unans = srp(Ether(dst=mac) / ARP(pdst=ipscan), timeout=2, verbose=False)
        # log.info(ans, unans)
    except Exception as e:
        log.info(str(e))
    else:
        for snd, rcv in ans:
            __mac = rcv.sprintf("%Ether.src%")
            ip = rcv.sprintf("%ARP.psrc%")
            arp_table[__mac] = ip
    log.info(arp_table)
    return arp_table


def islive(mac, times=3):
    mac = str.lower(mac)
    while times > 0:
        if mac in arp_scan(mac):
            return True
        else:
            times -= 1
            time.sleep(3)
            continue
    return False


def all_islive(list, times=3):
    for mac in list:
        flag = False
        if islive(mac,times):
            flag = True
            continue
        else:
            return flag
    return flag


@exception_handler
@retry(retries=3)
def get_ip(mac):
    __mac = str.lower(mac)
    # log.info(arp_scan(__mac))
    return arp_scan(__mac)[__mac]


if __name__ == '__main__':
    # print(all_islive(["5A:5A:00:42:44:40"]))
    # print(d.islive("5A:5A:00:3F:34:4D"))
    print(get_ip("5A:5A:00:56:4A:35"))
