def generate_secret_both(prime_number, base, private_a, private_b):
    public_a = base**private_a % prime_number
    public_b = base**private_b % prime_number
    secret_a = public_b**private_a % prime_number
    secret_b = public_a**private_b % prime_number
    return secret_a, secret_b

def generate_public(prime_number, base, private_self):
    return base**private_self % prime_number
    

def generate_secret(prime_number, public_other, private_self):
    return public_other**private_self % prime_number

def save_key(key, public=True):
    if public:
        f = open("public_key.pub", "w+")
        f.write(str(key))
        f.close()
    else:
        f = open("private_key.pri", "w+")
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
    
save_key((79,3337))
print(read_key(text="(79, 3337)"))
print(read_key(from_file=True, fname="public_key.pub"))