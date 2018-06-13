# -*- coding: utf-8 -*-

import hashlib
import base64
import random
import string

# string's md5
def str_md5(string):
    m2 = hashlib.md5()
    m2.update(string)
    md5 = m2.hexdigest()
    return md5


def rand_string(size):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, size))
    return salt
