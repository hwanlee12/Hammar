import crypto
import sys
sys.modules['Crypto'] = crypto
from firebase import firebase
import os.path
import hashlib

SALT_SIZE = 16  # This size is arbitrary
IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits

password2 = 'hwanl22'
password = password2.encode()

salt = os.urandom(SALT_SIZE)
testsalt = b'0912'
base = hashlib.pbkdf2_hmac('sha256', password, testsalt, 100000, dklen=IV_SIZE + KEY_SIZE)
iv = base[0:IV_SIZE]
key = base[IV_SIZE:]

firebase = firebase.FirebaseApplication('https://keydata-e5fb1.firebaseio.com/', None)

#result = firebase.post('/user'+'/'+ password2, {'ID':password2, 'IV':str(iv), 'KEY':str(key)})
#print(result)

#firebase = firebase.FirebaseApplication('https://keydata-e5fb1.firebaseio.com/', None)
#gimochi = firebase.post('/user/'+password2,{"IV" : str(base)})
users = firebase.get('/user/hwanlee', None)
print(list(users.values())[0]["IV"])

#ID = firebase.get('/user/test',None)
#print(ID)

#IV = firebase.get('/user', '-LmnL0J7Ur8aayKPTrw0').get('IV')
#print('IV = ' + IV)

