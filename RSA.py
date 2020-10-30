import math

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

def public_key(totient):
    for e in range(2, totient): 
        if gcd(e, totient)== 1:
            return e

def private_key(rsa_modulus, public_key):
    totient = eulers_totient_1(rsa_modulus)
    k = 1
    while True:
        mod = (1 + k*totient) % public_key
        if mod == 0:
            return int((1 + k*totient) / public_key)
        else:
            k += 1

def splitString(string_to_split, split_length):
    splittedStringList = []
    for i in range (0, len(string_to_split), split_length):
        splittedStringPart = string_to_split[i:i+split_length]
        splittedStringList.append(splittedStringPart)
    return splittedStringList

def encrypt_text(text, p, q, public_key):
    rsa_modulus = generate_rsa_modulus(p, q)
    encoded_textList = []
    for charIndex in range(len(text)):
        textPart = ""
        value = ord(text[charIndex])
        string_value = str(value)
        for i in range(len(string_value), len(str(1114111))):
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
        encrypted_textPart = str(pow(int(i), public_key, rsa_modulus))
        for i in range(len(encrypted_textPart), len(str(rsa_modulus))):
            encrypted_textPart = "0" + encrypted_textPart
        encrypted_textList.append(encrypted_textPart)
    return "".join(encrypted_textList)

def decrypted(text, p, q, private_key):
    rsa_modulus = generate_rsa_modulus(p, q)
    splitText = splitString(text, len(str(rsa_modulus)))
    decoded_text = ""
    decoded_textList = []
    for splitTextPart in splitText:
        decoded_splitTextPart = str(pow(int(splitTextPart), private_key, rsa_modulus))
        decoded_textList.append(decoded_splitTextPart)
    decoded_combined_textList = []
    for i in range(0, len(decoded_textList), math.ceil(len(str(1114111)) / len(str(rsa_modulus)))):
        decoded_combined_textList_part = ""
        for j in range(math.ceil(len(str(1114111)) / len(str(rsa_modulus)))):
            decoded_combined_textList_part += decoded_textList[i+j]
        decoded_combined_textList.append(decoded_combined_textList_part)
    decrypted_textList = []
    for i in decoded_combined_textList:
        decrypted_textList.append(chr(int(i)))
    return "".join(decrypted_textList)

# text = chr(1111)+chr(1112)+chr(3337)+chr(3338)+chr(0x10fffe)+chr(0x10ffff)
# encoded = encrypt_text(text, 47,71, 79)
# print(encoded)
# decoded = decrypted(encoded, 47,71, 1019)
# print(decoded)
# print(text)