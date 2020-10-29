def toUpperCase(text):
    return "".join(filter(str.isupper, text.upper()))

def splitString(string_to_split, split_length):
    splittedStringList = []
    for i in range (0, len(string_to_split), split_length):
        splittedStringPart = string_to_split[i:i+split_length]
        #print("splittedStringPart = ", splittedStringPart)
        splittedStringList.append(splittedStringPart)
    print("splittedStringList In Method = ", splittedStringList)
    return splittedStringList

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
            #print(k)
            return int((1 + k*totient) / public_key)
        else:
            k += 1
    
def gcd(p, q): 
    if(q == 0): 
        return p 
    else: 
        return gcd(q, p % q)

def encode_text(text):
    #text = toUpperCase(text)
    newTextList = []
    #alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    for i in range(len(text)):
        #idx = alphabet.index(text[i])
        idx = ord(text[i])
        print("text = " , text[i], " | index = ",  idx)
        if len(str(idx)) < 3:
            for i in range(len(str(idx)), 3):
                idx = "0" + str(idx)
        newTextList.append(str(idx))
    print("newTextList = ", newTextList)
    return "".join(newTextList)

def decode_text(text):
    splitted_text = splitString(text, 3)
    #alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    decoded_textList = []
    for charnum in splitted_text:
        #decoded_textList.append(alphabet[int(charnum)])
        decoded_textList.append(chr(int(charnum)))
    return "".join(decoded_textList)

def encrypt_text(text, p, q, public_key):
    n = rsa_modulus(p, q)
    block_length = len(str(n))
    encodedText = encode_text(text)
    textList = splitString(encodedText, block_length)
    totient = eulers_totient(p, q)
    encrypted_textList = []
    for i in textList:
        encrypted_encoded_textPart = pow(int(i), public_key) % n
        if len(str(encrypted_encoded_textPart)) < block_length:
            for i in range(len(str(encrypted_encoded_textPart)), block_length):
                encrypted_encoded_textPart = '0' + str(encrypted_encoded_textPart)
        encrypted_textList.append(str(encrypted_encoded_textPart))
    print("n = ", n)
    print("block_length = ", block_length)
    print("totient = ", totient)
    print("encrypted_textList = ", encrypted_textList)
    return "".join(encrypted_textList)

def decrypt_text(text, p, q, private_key):
    n = rsa_modulus(p, q)
    block_length = len(str(n))
    textList = splitString(text, block_length)
    totient = eulers_totient(p, q)
    decrypted_textList = []
    for textPart in textList:
        decrypted_encoded_textPart = pow(int(textPart), private_key) % n
        if len(str(decrypted_encoded_textPart)) < block_length:
            for i in range(len(str(decrypted_encoded_textPart)), block_length):
                decrypted_encoded_textPart = '0' + str(decrypted_encoded_textPart)
        decrypted_textList.append(str(decrypted_encoded_textPart))
    print("n = ", n)
    print("block_length = ", block_length)
    print("totient = ", totient)
    decrypted_decoded_text = decode_text("".join(decrypted_textList))
    return decrypted_decoded_text

encrypted = encrypt_text('HELLO ALICE', 47, 71, 79)
#encrypted = encrypt_text('HELLO ALICE', 961748941, 982451653, public_key(eulers_totient(961748941,982451653)))
print("encrypted = ", encrypted)
#print(encrypt_text('HELLO ALICE', 173, 199))
#print(encrypt_text('HELLO ALICE', 991, 997))
decrypted = decrypt_text(encrypted, 47, 71, private_key(rsa_modulus(47,71),79))
#decrypted = decrypt_text(encrypted, 961748941, 982451653, private_key(rsa_modulus(961748941, 982451653), public_key(eulers_totient(961748941,982451653))))
print("decrypted = ", decrypted)

# rsa_modulus = rsa_modulus(47,71)
# # eulers_totient = eulers_totient(47,71)
# # #public_key = public_key(eulers_totient)
# # public_key = 79
# # print("n = ", rsa_modulus)
# # print("totient = ", eulers_totient)
# # print("pubkey = ", public_key)
# print(private_key(rsa_modulus, 79))
# #print((1+25*3220) % 79)