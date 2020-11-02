import random
import math
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

class PrivateKey(object):
    def __init__(self, p=None, g=None, x=None, i_num_bits=0):
        self.p = p
        self.g = g
        self.x = x
        self.i_num_bits = i_num_bits
    
    def save(self, filename):
        f = open(filename, "w")
        f.write(str(self.p) + " " + str(self.g) + " " + str(self.x) + " " + str(self.i_num_bits))
        f.close()

    def read(self, filename):
        f = open(filename, "r")
        keys = f.read()
        f.close()
        keys = keys.split(" ")
        if(len(keys) < 4):
            print("Not a valid key file")
            return
        self.p = int(keys[0])
        self.g = int(keys[1])
        self.x = int(keys[2])
        self.i_num_bits = int(keys[3])

class PublicKey(object):
    def __init__(self, p=None, g=None, h=None, i_num_bits=0):
        self.p = p
        self.g = g
        self.h = h
        self.i_num_bits = i_num_bits

    def save(self, filename):
        f = open(filename, "w")
        f.write(str(self.p) + " " + str(self.g) + " " + str(self.h) + " " + str(self.i_num_bits))
        f.close()

    def read(self, filename):
        f = open(filename, "r")
        keys = f.read()
        f.close()
        keys = keys.split(" ")
        if(len(keys) < 4):
            print("Not a valid key file")
            return
        self.p = int(keys[0])
        self.g = int(keys[1])
        self.h = int(keys[2])
        self.i_num_bits = int(keys[3])

def gcd( a, b ):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def modexp( base, exp, modulus ):
    return pow(base, exp, modulus)

#solovay-strassen primality test.  tests if num is prime
def SS( num, i_confidence ):
    #ensure confidence of t
    for i in range(i_confidence):
        #choose random a between 1 and n-2
        a = random.randint( 1, num-1 )

        #if a is not relatively prime to n, n is composite
        if gcd( a, num ) > 1:
            return False

        #declares n prime if jacobi(a, n) is congruent to a^((n-1)/2) mod n
        if not jacobi( a, num ) % num == modexp ( a, (num-1)//2, num ):
            return False

    #if there have been t iterations without failure, num is believed to be prime
    return True

#computes the jacobi symbol of a, n
def jacobi( a, n ):
    if a == 0:
        if n == 1:
            return 1
        else:
            return 0
    #property 1 of the jacobi symbol
    elif a == -1:
        if n % 2 == 0:
            return 1
        else:
            return -1
    #if a == 1, jacobi symbol is equal to 1
    elif a == 1:
        return 1
    #property 4 of the jacobi symbol
    elif a == 2:
        if n % 8 == 1 or n % 8 == 7:
            return 1
        elif n % 8 == 3 or n % 8 == 5:
            return -1
    #property of the jacobi symbol:
    #if a = b mod n, jacobi(a, n) = jacobi( b, n )
    elif a >= n:
        return jacobi( a%n, n)
    elif a%2 == 0:
        return jacobi(2, n)*jacobi(a//2, n)
    #law of quadratic reciprocity
    #if a is odd and a is coprime to n
    else:
        if a % 4 == 3 and n%4 == 3:
            return -1 * jacobi( n, a)
        else:
            return jacobi(n, a )


#finds a primitive root for prime p
#this function was implemented from the algorithm described here:
#http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
def find_primitive_root( p ):
    if p == 2:
            return 1
    #the prime divisors of p-1 are 2 and (p-1)/2 because
    #p = 2x + 1 where x is a prime
    p1 = 2
    p2 = (p-1) // p1

    #test random g's until one is found that is a primitive root mod p
    while( 1 ):
        g = random.randint( 2, p-1 )
        #g is a primitive root if for all prime factors of p-1, p[i]
        #g^((p-1)/p[i]) (mod p) is not congruent to 1
        if not (modexp( g, (p-1)//p1, p ) == 1):
            if not modexp( g, (p-1)//p2, p ) == 1:
                return g

#find n bit prime
def find_prime(i_num_bits, i_confidence):
    #keep testing until one is found
    while(1):
        #generate potential prime randomly
        p = random.randint( 2**(i_num_bits-2), 2**(i_num_bits-1) )
        #make sure it is odd
        while( p % 2 == 0 ):
            p = random.randint(2**(i_num_bits-2),2**(i_num_bits-1))

        #keep doing this if the solovay-strassen test fails
        while( not SS(p, i_confidence) ):
            p = random.randint( 2**(i_num_bits-2), 2**(i_num_bits-1) )
            while( p % 2 == 0 ):
                p = random.randint(2**(i_num_bits-2), 2**(i_num_bits-1))

        #if p is prime compute p = 2*p + 1
        #if p is prime, we have succeeded; else, start over
        p = p * 2 + 1
        if SS(p, i_confidence):
                return p

def encode(string_plaintext, i_num_bits):
    byte_array = bytearray(string_plaintext, 'utf-16')
    z = []
    k = i_num_bits//8
    j = -1 * k
    num = 0
    for i in range(len(byte_array)):
        if i % k == 0:
            j += k
            num = 0
            z.append(0)
        z[j//k] += byte_array[i]*(2**(8*(i%k)))
    return z

def decode(integers_plaintext, i_num_bits):
    bytes_array = []
    k = i_num_bits//8

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

def generate_keys(i_num_bits=256, i_confidence=32):
    p = find_prime(i_num_bits, i_confidence)
    g = find_primitive_root(p)
    g = modexp( g, 2, p )
    x = random.randint( 1, (p - 1) // 2 )
    h = modexp( g, x, p )

    public_key = PublicKey(p, g, h, i_num_bits)
    private_key = PrivateKey(p, g, x, i_num_bits)

    return {'privateKey': private_key, 'publicKey': public_key}

def encrypt(key, string_plaintext):
    z = encode(string_plaintext, key.i_num_bits)
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

def decrypt(key, cipher):
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

    decrypted = decode(plaintext, key.i_num_bits)
    decrypted = "".join([char for char in decrypted if char != '\x00'])
    return decrypted

def test():
    assert (sys.version_info >= (3,4))
    #keys = generate_keys()
    #priv = keys['privateKey']
    #pub = keys['publicKey']
    priv = PrivateKey()
    priv.read("key.pri")
    pub = PublicKey()
    pub.read("key.pub")
    #message = readFile("example.txt")
    message = "Killer queen has already touched the doorknob"
    cipher = encrypt(pub, message)
    #cipher = readFile("enc.txt")
    plain = decrypt(priv, cipher)
    print(cipher)
    print(plain)

    return message == plain

test()