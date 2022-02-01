from random import randint, choice
from string import ascii_lowercase, digits

def get_random_string(a, b):
    return ''.join([choice(ascii_lowercase+digits) for _ in range(randint(a, b))])

def get_random_float(a, b):
    return float(f"{randint(a, b)}.{randint(0, 99)}")
