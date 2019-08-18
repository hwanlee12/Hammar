shared_prime = 23 #N
shared_base = 5 #G

A_secret = 6 #a
B_secret = 15 #b

print("Publicly Shared Prime :", shared_prime)
print("Publicly Shared Base : ", shared_base)
//
A_public = (shared_base**A_secret) % 23
print("A pub key : ", A_public)
print("A priv key : ", A_secret)

B_public = (shared_base**B_secret) % 23
print("B pub key : ", B_public)
print("B priv key : ", B_secret)

A_final = (B_public**A_secret) % 23
print("A session key : ", A_final)

B_final = (A_public**B_secret) % 23
print("B session key : ", B_final)
