import hashlib, uuid

def createKey(prefix):
    return prefix + uuid.uuid1().hex().replace('-', '')

def createUuid():
    return uuid.uuid1().hex().replace('-', '')