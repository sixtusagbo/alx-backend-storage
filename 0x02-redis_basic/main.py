#!/usr/bin/env python3
""" Main file """
import redis
import time

get_page = __import__('web').get_page
_redis = redis.Redis()

url = "http://google.com"
count_key = "count:{}".format(url)
print('get_page result:')
print(get_page(url))
print()
print('------------------------------------------------------')
print("{}: {}".format(count_key, int(_redis.get(count_key))))
time.sleep(3)
print("ttl after 3s: {}".format(_redis.ttl(url)))
