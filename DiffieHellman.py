from Crypto.Util import number

bit = 20

def generate_secret_both(prime_number, base, private_a, private_b):
    prime_number = int(prime_number)
    base = int(base)
    private_a = int(private_a)
    private_b = int(private_b)
    public_a = base**private_a % prime_number
    public_b = base**private_b % prime_number
    secret_a = public_b**private_a % prime_number
    secret_b = public_a**private_b % prime_number
    if secret_a != secret_b:
        raise ValueError(secret_a + "!=" + secret_b)
    return secret_a

def generate_prime(bit):
    prime_number = number.getPrime(bit)
    return prime_number

def generate_prime_less_than_n(bit, n):
    prime_number = number.getPrime(bit)
    while n >= prime_number:
        prime_number = number.getPrime(bit)
    return prime_number

# prime_number = generate_prime(bit)
# print("prime =",prime_number)
# base = generate_prime_less_than_n(bit, prime_number)
# print("base = ",base)

# private_a = number.getRandomInteger(bit)
# print("a = ",private_a)
# private_b = number.getRandomInteger(bit)
# print("b = ", private_b)
# secret = generate_secret_both(prime_number, base, private_a, private_b)
# print(secret)
    
# # save_key((79,3337))
# # print(read_key(text="(79, 3337)"))
# # print(read_key(from_file=True, fname="public_key.pub"))
# # print(generate_prime(1024))