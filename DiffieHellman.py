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
        f.write(key)
        f.close()
    else:
        f = open("private_key.pri", "w+")
        f.write(key)
        f.close()