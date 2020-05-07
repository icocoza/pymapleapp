
from Crypto.Cipher import Blowfish
from Crypto import Random
from struct import pack
import base62

class CryptoHelper:
    KEY = b'KOREAN_GEO_GRAPHICS_ON_KBS2_1001'
    BS = Blowfish.block_size

    def enc(self, text):
        iv = Random.new().read(BS)
        cipher = Blowfish.new(KEY, Blowfish.MODE_CBC, iv)
        plen = BS - divmod(len(text), BS)[1]
        padding = [plen]*plen
        padding = pack('b'*plen, *padding)
        ciphertext = iv + cipher.encrypt(text + padding)
        return base62.encodebytes(ciphertext)

    def dec(self, text):
        ciphertext = base62.decodebytes(text)
        iv = ciphertext[:BS]
        ciphertext = ciphertext[BS:]
        cipher = Blowfish.new(KEY, Blowfish.MODE_CBC, iv)
        msg = cipher.decrypt(ciphertext)

        last_byte = msg[-1]
        msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
        return repr(msg)
