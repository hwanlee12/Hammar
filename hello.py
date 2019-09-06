from Cryptodome.Cipher import AES
import firebase
from firebase_admin import db
from firebase import firebase
import os.path
import struct
import hashlib
import ctypes
import json
SALT_SIZE = 16  # This size is arbitrary
IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits


password2 = 'hwan'
password = password2.encode()

salt = os.urandom(SALT_SIZE)
testsalt = b'0912'
base = hashlib.pbkdf2_hmac('sha256', password, testsalt, 100000, dklen=IV_SIZE + KEY_SIZE)

firebase = firebase.FirebaseApplication('https://keydata-e5fb1.firebaseio.com/', None)
gimochi = firebase.post('/user/'+password2,str(base))
users = firebase.get('/user/'+password2,None)
hawi2 = list(users.values())[0]["IV"][1:]
hawi = hawi2.encode()
print(base[0])
print(hawi[0])

#a -> id == mac a -> iv a ->key
#b -> id 
