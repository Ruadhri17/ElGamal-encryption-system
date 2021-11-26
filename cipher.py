import sys
from random import randint
from math import pow, sqrt

def isPrime(n):
    if n == 2:
        return True
    
    if n % 2 == 0 or n <= 1:
        return False
    
    sqr = int(sqrt(n)) + 1
    
    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True

def cyclicGroupDescription(p):
    #Calculate order
    q = p - 1
    #Get generator
    for g in range(1, q): 
        if (pow(g, q) % p) == 1:
            break;          
    return (p, q, g) 

def generateKey(p, q, g):
    x = randint(1, q - 1) # Private Key
    h = pow(g, x)
    publicKey = (p, q, g, h)
    privateKey = x
    return (publicKey, privateKey)

def encryption(message, key):
    m = map(message)
    y = randint(1, key[1])
    s = pow(key[3], y)
    c1 = pow(key[2], y)
    c2 = m * s
    return
def decryption(message, key):
    return
    
def main():
    try:
        value = int(input("Choose cyclic group size (enter prime number): "))
    except ValueError:
        print("Input is not valid!")
        return
    if isPrime(value) == False:
        print("Input is not prime number!")
        return
    else:
        (group , order , generator) = cyclicGroupDescription(value)
        (publicKey, privateKey) = generateKey(group, order, generator)
        encryption(message, publicKey)
        decryption(privateKey)
        return

if __name__ == "__main__":
    main()