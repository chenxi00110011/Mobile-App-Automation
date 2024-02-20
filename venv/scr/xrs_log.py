import builtins
import logging as log
import xrs_time
from environment_variable import filename

log.basicConfig(filename=f'{filename}{xrs_time.today()}.log', level=log.INFO)


def log_info(msg,falg =True):
    result = xrs_time.get_current_time()+'\t' + msg
    if falg:
        print(result)
    log.info(result)


def print(*args):
    if True:
        for i in args:
            builtins.print(i,end='')
        builtins.print()