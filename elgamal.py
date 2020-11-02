import math
import random
import sys

def readFile(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text

def writeFile(filename, text):
    f = open(filename, "w")
    f.write(text)
    f.close()

class PublicKey(object):
    def __init__(self, p=None, g=None, h=None, n_bits=0):
        self.p = p
        self.g = g
        self.h = h
        self.n_bits = n_bits

    def save(self, filename="elgamal_public_key.pub"):
        f = open(filename, "w")
        f.write(str(self.p) + " " + str(self.g) + " " + str(self.h) + " " + str(self.n_bits))
        f.close()

    def read(self, filename):
        f = open(filename, "r")
        keys = f.read()
        f.close()
        self.fromText(keys)

    def fromText(self, keys):
        keys = keys.split(" ")
        if(len(keys) < 4):
            print("Not a valid key file")
            return
        self.p = int(keys[0])
        self.g = int(keys[1])
        self.h = int(keys[2])
        self.n_bits = int(keys[3])

class PrivateKey(object):
    def __init__(self, p=None, g=None, x=None, n_bits=0):
        self.p = p
        self.g = g
        self.x = x
        self.n_bits = n_bits
    
    def save(self, filename="elgamal_private_key.pri"):
        f = open(filename, "w")
        f.write(str(self.p) + " " + str(self.g) + " " + str(self.x) + " " + str(self.n_bits))
        f.close()

    def read(self, filename):
        f = open(filename, "r")
        keys = f.read()
        f.close()
        self.fromText(keys)

    def fromText(self, keys):
        keys = keys.split(" ")
        if(len(keys) < 4):
            print("Not a valid key file")
            return
        self.p = int(keys[0])
        self.g = int(keys[1])
        self.x = int(keys[2])
        self.n_bits = int(keys[3])

# finds the jacobi symbol of a, n
def jacobi( a, n ):
    if a == 0:
        if n == 1:
            return 1
        else:
            return 0
    elif a == -1:
        if n % 2 == 0:
            return 1
        else:
            return -1
    elif a == 1:
        return 1
    elif a == 2:
        if n % 8 == 1 or n % 8 == 7:
            return 1
        elif n % 8 == 3 or n % 8 == 5:
            return -1
    elif a >= n:
        return jacobi( a%n, n)
    elif a%2 == 0:
        return jacobi(2, n)*jacobi(a//2, n)
    else:
        if a % 4 == 3 and n%4 == 3:
            return -1 * jacobi(n, a)
        else:
            return jacobi(n, a)

# solovay-strassen primality test to check whether or not num is prime
def SS(num, confidence):
    for i in range(confidence):
        a = random.randint( 1, num-1 )
        if gcd( a, num ) > 1:
            return False

        if not jacobi( a, num ) % num == modexp ( a, (num-1)//2, num ):
            return False

    return True

# greatest common divisor of a and b
def gcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def modexp(base, exp, modulus):
    return pow(base, exp, modulus)


# finds a primitive root for prime number p
# algorithm described here: http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p-1) // p1

    while( 1 ):
        g = random.randint(2, p-1)
        if not (modexp(g, (p-1)//p1, p) == 1):
            if not modexp(g, (p-1)//p2, p) == 1:
                return g

# finds n bit prime number
def find_prime(n_bits, confidence):
    while(1):
        p = random.randint( 2**(n_bits-2), 2**(n_bits-1) )
        while(p % 2 == 0):
            p = random.randint(2**(n_bits-2),2**(n_bits-1))

        while(not SS(p, confidence)):
            p = random.randint(2**(n_bits-2), 2**(n_bits-1))
            while( p % 2 == 0 ):
                p = random.randint(2**(n_bits-2), 2**(n_bits-1))

        p = p * 2 + 1
        if SS(p, confidence):
                return p

# encode string plaintext to integer form
def encode(string_plaintext, n_bits):
    byte_array = bytearray(string_plaintext, 'utf-16')
    z = []
    k = n_bits//8
    j = -1 * k
    num = 0
    for i in range(len(byte_array)):
        if i % k == 0:
            j += k
            num = 0
            z.append(0)
        z[j//k] += byte_array[i]*(2**(8*(i%k)))
    return z

# decode integer plaintext to string form
def decode(integers_plaintext, n_bits):
    bytes_array = []
    k = n_bits//8

    for num in integers_plaintext:
        for i in range(k):
            temp = num
            for j in range(i+1, k):
                temp = temp % (2**(8*j))
            letter = temp // (2**(8*i))
            bytes_array.append(letter)
            num = num - (letter*(2**(8*i)))
    decoded = bytearray(b for b in bytes_array).decode('utf-16')
    return decoded

# generate public key and private key
def generate_keys(n_bits=256, confidence=32):
    p = find_prime(n_bits, confidence)
    g = find_primitive_root(p)
    g = modexp(g, 2, p)
    x = random.randint(1, (p - 1) // 2)
    h = modexp(g, x, p)

    public_key = PublicKey(p, g, h, n_bits)
    private_key = PrivateKey(p, g, x, n_bits)

    return {'privateKey': private_key, 'publicKey': public_key}

def encrypt(string_plaintext, key):
    z = encode(string_plaintext, key.n_bits)
    cipher_pairs = []
    for i in z:
        y = random.randint( 0, key.p )
        c = modexp( key.g, y, key.p )
        d = (i*modexp( key.h, y, key.p)) % key.p
        cipher_pairs.append( [c, d] )

    encrypted = ""
    for pair in cipher_pairs:
        encrypted += str(pair[0]) + ' ' + str(pair[1]) + ' '

    return encrypted

def decrypt(cipher, key):
    plaintext = []

    cipher_array = cipher.split()
    if (not len(cipher_array) % 2 == 0):
        return "malformed cipher text"
    for i in range(0, len(cipher_array), 2):
        first = int(cipher_array[i])
        second = int(cipher_array[i+1])

        s = modexp( first, key.x, key.p )
        plain = (second*modexp(s, key.p-2, key.p)) % key.p
        plaintext.append(plain)

    decrypted = decode(plaintext, key.n_bits)
    decrypted = "".join([char for char in decrypted if char != '\x00'])
    return decrypted

def test():
    assert (sys.version_info >= (3,4))
    #keys = generate_keys()
    #pri = keys['privateKey']
    #pub = keys['publicKey']
    pri = PrivateKey()
    pri.read("elgamal_private_key.pri")
    pub = PublicKey()
    pub.read("elgamal_public_key.pub")
    #message = readFile("example.txt")
    message = "King Crimson"
    cipher = encrypt(message, pub)
    #cipher = readFile("enc.txt")
    plain = decrypt(cipher, pri)
    print(cipher)
    print(plain)

    return message == plain