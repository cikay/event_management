import random

def generate_random_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxy_123456789'
    return ''.join((random.choice(sample_string)) for _ in range(length))
