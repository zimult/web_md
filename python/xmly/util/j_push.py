# -*- coding: utf-8 -*-

import hashlib
import base64
import random
import string
import jpush
import traceback


jpush_app_key = "8c5e6ca676b8c1a9910615b5"
jpush_master_secret = "c1464c6ac4502530f722c541"

_jpush = jpush.JPush(jpush_app_key, jpush_master_secret)
push = _jpush.create_push()

# if you set the logging level to "DEBUG",it will show the debug logging.
_jpush.set_logging("DEBUG")

#push.audience = jpush.all_
#push.platform = jpush.all_
push.audience = jpush.audience(jpush.registration_id('191e35f7e01344072f8'))

push.platform = jpush.platform('ios')

ios = jpush.ios(alert="Hello, 专辑推送测试",  extras={"type":"3","id":"16302530","ios":{"sound":"default","badge":1}})
android = jpush.android(alert="Hello, 专辑推送测试", priority=1, style=1, alert_type=1, extras={"type":"3","id":"16302530","ios":{"sound":"default","badge":1}})

#push.notification = jpush.notification(alert="Hello, JPush!", android=android, ios=ios)
push.notification = jpush.notification(alert="Hello, JPush!", ios=ios)

# pprint (push.payload)
result = push.send()


