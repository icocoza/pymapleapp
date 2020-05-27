import hashlib, uuid
import time

def createKey(prefix):
    return prefix + str(uuid.uuid1()).replace('-', '') + str(int(round(time.time() * 1000)))

def createUuid():
    return str(uuid.uuid1()).replace('-', '')