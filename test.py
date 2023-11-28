import hashlib

a = "abc".encode("utf-8")
p = hashlib.sha512(a).hexdigest()
print(p)
print(len(p))
