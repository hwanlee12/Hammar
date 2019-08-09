from Crypto.Cipher import AES
import os
import hashlib

IV_SIZE = 16    # 128 bit, fixed for the AES algorithm
KEY_SIZE = 32   # 256 bit meaning AES-256, can also be 128 or 192 bits
SALT_SIZE = 16  # This size is arbitrary

cleartext = b'Lorem ipsum'
password = b'highly secure encryption password'
salt = os.urandom(SALT_SIZE)
derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                              dklen=IV_SIZE + KEY_SIZE)
iv = derived[0:IV_SIZE]
key = derived[IV_SIZE:]

encrypted = salt + AES.new(key, AES.MODE_CFB, iv).encrypt(cleartext)

salt = encrypted[0:SALT_SIZE]
derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                              dklen=IV_SIZE + KEY_SIZE)
iv = derived[0:IV_SIZE]
key = derived[IV_SIZE:]
cleartext = AES.new(key, AES.MODE_CFB, iv).decrypt(encrypted[SALT_SIZE:])

print("key", key)
print("plaintext", cleartext)
print("ciphertext", encrypted)

inFp, outFp = None, None
inStr, outStr = "", ""

i = 0
secu = 0

select = int(input("1.암호화  2.암호 해석 중 선택 : "))
inFname = input("입력 파일명을 입력하세요 : ")
outFname = input("출력 파일명을 입력하세요 : ")

if select == 1:
    secu = 100
elif select == 2:
    secu = -100

inFp = open(inFname, "r", encoding="utf-8")
outFp = open(outFname, "w", encoding="utf-8")

while True:
    inStr = inFp.readline()
    print(inStr)
    if not inStr:
        ##문자열 객체 하나도 없으면 True반환
        break

    outStr = ""

    for i in range(0, len(inStr)):
        ch = inStr[i]
        chNum = ord(ch)
        chNum = chNum + secu
        ch2 = chr(chNum)
        outStr += ch2

    outFp.write(outStr)

outFp.close()
inFp.close()
print("%s --> %s 변환 " % (inFname, outFname))