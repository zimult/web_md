ps -ef | grep gunicorn | grep api | awk '{print $2}' | xargs kill -9

nohup gunicorn -w 4 -b 0.0.0.0:8410 --access-logfile log/qy.log --access-logformat "%(h)s %(p)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(L)s" api:shorty_api &
