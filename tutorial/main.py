from functools import lru_cache
import time


@lru_cache()
def my_expensive_function(a, ttl_hash=None):
    print("wait")
    print(a)
    del ttl_hash
    return a# to emphasize we don't use it and to shut pylint up


def get_ttl_hash(seconds=3):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


# somewhere in your code...
res = my_expensive_function("hello", ttl_hash=get_ttl_hash())
print("got", res)
time.sleep(2)

res = my_expensive_function("hello", ttl_hash=get_ttl_hash())
print("got", res)
time.sleep(2)

res = my_expensive_function("test", ttl_hash=get_ttl_hash())
print("got", res)
time.sleep(2)

res = my_expensive_function("test", ttl_hash=get_ttl_hash())
print("got", res)
time.sleep(2)
