from Crypto.Cipher import AES
import os
import hashlib
import base64

IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits
SALT_SIZE = 16  # This size is arbitrary

plaintext = input('평문 입력 : ')
password = input('base 입력 : ')
password = password.encode()

#salt = os.urandom(SALT_SIZE)
salt = b'1'
base = hashlib.pbkdf2_hmac('sha256', password, salt, 100, dklen=IV_SIZE + KEY_SIZE)
print('hash ', base)
iv = base[0:IV_SIZE]
key = base[IV_SIZE:]

print('iv', iv)
print('key : ', key)
plaintext3 =b'aa'
plaintext3 = base64.b64encode(plaintext3)
temp = base64.b64decode(plaintext3)
print('plain', temp)

plaintext = plaintext.encode()
ciphertext = AES.new(key, AES.MODE_CFB, iv).encrypt(plaintext)
print("ciphertext : ", ciphertext)
plaintext2 = AES.new(key, AES.MODE_CFB, iv).decrypt(ciphertext)
plaintext2 = plaintext2.decode()
print('plaintext : ', plaintext2)
