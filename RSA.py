import math
from Crypto.Util import number

bit = 8
max_ord = 1114111

def generate_rsa_modulus(p, q):
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

def generate_public_key(p, q):
    p = int(p)
    q = int(q)
    totient = eulers_totient(p,q)
    print("totient = ", totient)
    rsa_modulus = generate_rsa_modulus(p,q) 
    for e in range(2, totient): 
        if gcd(e, totient)== 1:
            return e, rsa_modulus

#public key = (encryption_key, rsa_modulus) -> tuple
def generate_private_key(public_key):
    encryption_key, rsa_modulus = public_key
    encryption_key = int(encryption_key)
    rsa_modulus = int(rsa_modulus)
    totient = eulers_totient_1(rsa_modulus)
    k = 1
    while True:
        mod = (1 + k*totient) % encryption_key
        if mod == 0:
            return int((1 + k*totient) / encryption_key), rsa_modulus
        else:
            k += 1

def generate_random_public_key(prime_number_bit):
    public_key = None
    e = 6
    rsa_modulus = 6
    p_a = 0
    q_a = 0
    print(eulers_totient_1(rsa_modulus))
    while (public_key == None) or e % rsa_modulus == 0 or rsa_modulus % e == 0 or e % eulers_totient_1(rsa_modulus)== 0:
        while p_a == q_a:
            p_a = number.getPrime(prime_number_bit)
            q_a = number.getPrime(prime_number_bit)
        public_key = generate_public_key(p_a, q_a)
        if public_key != None:
            e, rsa_modulus = public_key
    return public_key

def generate_and_save_random_public_key(prime_number_bit, name="rsa_public_key.pub"):
    public_key = generate_random_public_key(prime_number_bit)
    save_key(public_key, name,public=True)
    return public_key

def generate_and_save_private_key(public_key, name="rsa_private_key.pri"):
    private_key = generate_private_key(publickeyA)
    save_key(private_key, name, public=False)
    return private_key

def splitString(string_to_split, split_length):
    splittedStringList = []
    for i in range (0, len(string_to_split), split_length):
        splittedStringPart = string_to_split[i:i+split_length]
        splittedStringList.append(splittedStringPart)
    return splittedStringList

def encrypt_text(text, public_key):
    encryption_key, rsa_modulus = public_key
    encryption_key = int(encryption_key)
    rsa_modulus = int(rsa_modulus)
    encoded_textList = []
    for charIndex in range(len(text)):
        textPart = ""
        value = ord(text[charIndex])
        string_value = str(value)
        for i in range(len(string_value), len(str(max_ord))):
            string_value = "0" + string_value
        extra = False
        for index in range(len(string_value)):
            if int(textPart+string_value[index]) < rsa_modulus and len(textPart) < len(str(rsa_modulus)):
                textPart += string_value[index]
            else:
                encoded_textList.append(textPart)
                textPart = string_value[index]
        encoded_textList.append(textPart)
    encrypted_textList = []
    for i in encoded_textList:
        encrypted_textPart = str(pow(int(i), encryption_key, rsa_modulus))
        for i in range(len(encrypted_textPart), len(str(rsa_modulus))):
            encrypted_textPart = "0" + encrypted_textPart
        encrypted_textList.append(encrypted_textPart)
    return "".join(encrypted_textList)

def decrypt_text(text, private_key):
    decryption_key, rsa_modulus = private_key
    decryption_key = int(decryption_key)
    rsa_modulus = int(rsa_modulus)
    splitText = splitString(text, len(str(rsa_modulus)))
    decoded_text = ""
    decoded_textList = []
    for splitTextPart in splitText:
        decoded_splitTextPart = str(pow(int(splitTextPart), decryption_key, rsa_modulus))
        decoded_textList.append(decoded_splitTextPart)
    decoded_combined_textList = []
    for i in range(0, len(decoded_textList), math.ceil(len(str(max_ord)) / len(str(rsa_modulus)))):
        decoded_combined_textList_part = ""
        for j in range(math.ceil(len(str(max_ord)) / len(str(rsa_modulus)))):
            decoded_combined_textList_part += decoded_textList[i+j]
        decoded_combined_textList.append(decoded_combined_textList_part)
    decrypted_textList = []

    for i in decoded_combined_textList:
        decrypted_textList.append(chr(int(i)))
    return "".join(decrypted_textList)

def save_key(key, name, public=True):
    if public:
        f = open(name, "w+")
        f.write(str(key))
        f.close()
    else:
        f = open(name, "w+")
        f.write(str(key))
        f.close()

def read_key(text="", from_file=False, fname=""):
    if not from_file:
        ds_string = text
    else:
        with open(fname, 'r') as f:
            ds_string = f.read()
    retreived_ds = []
    i = 0
    while(i < len(ds_string)):
        if ds_string[i] == '(':
            end_index = ds_string[i+1:].index(')') + i
            first, second = ds_string[i+1:end_index+1].split(',')
            retreived_ds.append((first.strip().replace("'", ""), second.strip().replace("'", "")))
            i = end_index + 1
        i = i + 1
    return retreived_ds[0]

# publickeyA = generate_and_save_random_public_key(bit)
# e, n = publickeyA
# print("eulers totient = ",eulers_totient_1(n))
# retrieved_key = read_key(from_file=True, fname="rsa_public_key.pub")
# print(publickeyA)
# print(retrieved_key)
# privatekeyA = generate_and_save_private_key(publickeyA)
# print("private_key=",privatekeyA)
# retrieved_pri_key = read_key(from_file=True, fname="rsa_private_key.pri")
# print(retrieved_pri_key)

# text = chr(1111)+chr(1112)+chr(3337)+chr(3338)+chr(0x10fffe)+chr(0x10ffff)
# encoded = encrypt_text(text, publickeyA)
# print(encoded)
# print(len(encoded))
# decoded = decrypt_text(encoded, privatekeyA)
# decoded = decrypt_text(encoded, privatekeyA)
# print(decoded)

# encoded = encrypt_text(text, 47,71, 79)
# print(encoded)
# decoded = decrypt_text(encoded, 47,71, 1019)
# print(decoded)
# print(text)
# public_key = (79, generate_rsa_modulus(47,71))
# encryption_key, rsa_modulus = public_key
# print(encryption_key)
# print(rsa_modulus)