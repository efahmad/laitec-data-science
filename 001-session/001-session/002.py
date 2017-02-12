import random
import string

lower = string.ascii_lowercase
upper = string.ascii_uppercase
digit = string.digits

p = random.choice(lower) + random.choice(upper) + random.choice(digit)

for _ in range(5):
    p += random.choice(lower+upper+digit)

p = list(p)
random.shuffle(p)
print(''.join(p))

