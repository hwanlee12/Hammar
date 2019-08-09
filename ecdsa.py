from Crypto.Cipher import AES
import os
import hashlib

IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits
SALT_SIZE = 16  # This size is arbitrary

#cleartext = b'Lorem ipsum'
#encrypted = salt + AES.new(key, AES.MODE_CFB, iv).encrypt(cleartext)
#salt = encrypted[0:SALT_SIZE]
#key = input("key : ")
#iv = input('iv : ')

plaintext = input('평문 입력 : ')
password = input('base 입력 : ')
password = password.encode()

salt = b'0'
base = hashlib.pbkdf2_hmac('sha256', password, salt, 100000, dklen=IV_SIZE + KEY_SIZE)
print('hash ',base)
iv = base[0:IV_SIZE]
key = base[IV_SIZE:]
print(len(base))
print('iv', iv)
print('key : ', key)

plaintext = plaintext.encode()
#ciphertext = AES.new(key, AES.MODE_EAX).encrypt(plaintext)
ciphertext = AES.new(key, AES.MODE_EAX)
print("ciphertext : ", ciphertext)
plaintext2 = AES.new(key, AES.MODE_EAX).decrypt(ciphertext)
print(plaintext2 == plaintext)
# plaintext2 = plaintext2.decode()
print('plaintext : ', plaintext2)
