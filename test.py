import random, string

def generate_salt():
    characters = string.ascii_letters + string.digits + string.punctuation
    salt = [random.choice(characters) for i in range(32)]
    return "".join(salt)

p = generate_salt()
print("kys"+p)