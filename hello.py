import crypto
import sys
sys.modules['Crypto'] = crypto
from firebase import firebase
import os.path
import hashlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

SALT_SIZE = 16  # This size is arbitrary
IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits

#cred = credentials.Certificate('keydata-e5fb1-export.json')
#firebase_admin = firebase_admin.initialize_app(cred, {'databaseURL' : 'https://keydata-e5fb1.firebaseio.com/'})

password = 'hwanl22'
password = password.encode()

salt = os.urandom(SALT_SIZE)
testsalt = b'0912'
base = hashlib.pbkdf2_hmac('sha256', password, testsalt, 100000, dklen=IV_SIZE + KEY_SIZE)
iv = base[0:IV_SIZE]
key = base[IV_SIZE:]

firebase = firebase.FirebaseApplication('https://keydata-e5fb1.firebaseio.com/', None)

#result = firebase.post('/user', {'ID':str(password),'IV':str(iv),'KEY':str(key)})
#print(result)

result2 = firebase.get('/user', None)
print(result2)



ID = firebase.get('/user', '-LmnL0J7Ur8aayKPTrw0').get('ID')
print('ID = ' + ID)

IV = firebase.get('/user', '/-LmnL0J7Ur8aayKPTrw0').get('IV')
print('IV = ' + IV)

Key = firebase.get('/user', '-LmnL0J7Ur8aayKPTrw0').get('KEY')
print('KEY = ' + Key)
