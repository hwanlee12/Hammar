def gcd(a, b): # 서로소인지 판단
    while b != 0:
        a, b = b, a % b
    return a

def decrypt(pk, ciphertext): # 복호화 과정
    #Unpack the key into its components
    key, n = pk # pk = (d, n)
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext] # P = (C^d) % n = (M^e*d) % n
    #Return the array of bytes as a string
    return ''.join(plain) # 평문

def encrypt(pk, plaintext): # 암호화 과정
    #Unpack the key into it's components
    key, n = pk # pk = (e, n)
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext] # C = (M^e) % n 반복
    #Return the array of bytes
    return cipher #암호문

def get_private_key(e, tot): # 비밀키 생성
    d = 1 # ed = 1 % ((p-1)*(q-1))를 만족하는 d(dec_key)를 찾기 전 초기화
    while (e * d) % tot != 1 or d == e: # 1부터 증가하면서 반복
        d += 1
    return d

def get_public_key(tot): # 공개키 생성
    e = 2 # (p-1)(q-1)과 서로소인 수 e(enc_key)를 초기화
    while e < totient and gcd(e, totient) != 1: # 반복문을 돌리면서 서로소인지 판단
        e += 1
    return e

# Input message to be encrypted
m = input("Enter the text to be encrypted:")

# Step 1. Choose two prime numbers
p = 311
q = 503

print("공개ㄴㄴ (p and q):", str(p), "and", str(q))

# Step 2. Compute n = pq which is the modulus of both the keys
n = p*q
print("공개ㄱㄴ n(p * q) =", str(p), "*", str(q), "=", str(n))

# Step 3. Calculate totient
totient = (p-1) * (q-1)
print("공개ㄴㄴ totient : (p-1) * (q-1) = ", str(totient))

# Step 4. Find public key e
e = get_public_key(totient)
print("Pub key(n, e):("+str(n)+","+str(e)+")")

# Step 5. Find private key d
d = get_private_key(e, totient)
print("Priv key(n, d):("+str(n)+","+str(d)+")")

# Step 6.Encrypt message
encrypted_msg = encrypt((e, n), m)
print('Encrypted Message:', ''.join(map(lambda x: str(x), encrypted_msg)))

# Step 7.Decrypt message
print('Decrypted Message:', decrypt((d, n), encrypted_msg))