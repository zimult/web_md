# -*- coding: utf-8 -*-

import random
import uuid
import time

def rand_code(length):
    number = '0123456789'
    id = ''
    for i in range(0, length):
        id += random.choice(number)
    print id
    return id


def randfilename():
    uuid_str = str(uuid.uuid1())
    date_str = time.strftime("%Y%m%d", time.localtime())
    return date_str + uuid_str.replace('-','')

def rand_timestr():
    uuid_str = str(uuid.uuid1())
    date_str = time.strftime("%y%m%d%H%M%S", time.localtime())
    return date_str + uuid_str.replace('-', '')


def rand_uuid():
    uuid_str = str(uuid.uuid1())
    return uuid_str.replace('-','')