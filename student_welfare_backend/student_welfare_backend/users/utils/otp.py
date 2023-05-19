from random import randint

def generate_otp():
    value = ""
    for i in range(6):
        value += str(randint(0,9))
    return value