# -*- coding: utf-8 -*-

import hashlib
import base64

# string's md5
def str_md5(string):
    m2 = hashlib.md5()
    m2.update(string)
    md5 = m2.hexdigest()
    return md5

