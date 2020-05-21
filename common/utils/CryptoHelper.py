
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
 
import base62

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

PASSWORD = 'KOREAN_GEO_GRAPHICS_ON_KBS2_1001'

def encrypt(plainText):
    private_key = hashlib.sha256(PASSWORD.encode("utf-8")).digest()
    plainText = pad(plainText)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    #return base64.b64encode(iv + cipher.encrypt(raw))
    return base62.encodebytes(iv + cipher.encrypt(plainText))


def decrypt(cipherText):
    private_key = hashlib.sha256(PASSWORD.encode("utf-8")).digest()
    #enc = base64.b64decode(enc)
    enc = base62.decodebytes(cipherText)
    iv = cipherText[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(cipherText[16:]))
