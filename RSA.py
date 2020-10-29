def rsa_modulus(p, q):
    return p * q

def eulers_totient(p, q):
    return (p-1)*(q-1)

def eulers_totient_1(x):
    if x == 1:
        return 1
    else:
        n = [y for y in range(1,x) if gcd(x,y)==1]
        return len(n)

def gcd(p, q): 
    if(q == 0): 
        return p 
    else: 
        return gcd(q, p % q)

def public_key(totient):
    for e in range(2, totient): 
        if gcd(e, totient)== 1:
            return e

def private_key(rsa_modulus, public_key):
    totient = eulers_totient_1(rsa_modulus)
    print(totient)
    k = 1
    while True:
        mod = (1 + k*totient) % public_key
        if mod == 0:
            return int((1 + k*totient) / public_key)
        else:
            k += 1

def encrypt_text(text, p, q, public_key):
    n = rsa_modulus(p, q)
    cipher = ""
    for char in text:
        value = ord(char)
        cipherpart = pow(value, public_key, n)
        cipherpart = chr(cipherpart)
        cipher += cipherpart
    return cipher

def decrypt_text(text, p, q, private_key):
    n = rsa_modulus(p, q)
    decipher = ""
    for char in text:
        value = ord(char)
        decipherpart = pow(value, private_key, n)
        decipherpart = chr(decipherpart)
        decipher += decipherpart
    return decipher

cipher = encrypt_text("AB", 47, 71, 79)
print("cipher = ", cipher)
decipher = decrypt_text(cipher, 47, 71, private_key(rsa_modulus(47,71),79))
print("decipher = ", decipher)