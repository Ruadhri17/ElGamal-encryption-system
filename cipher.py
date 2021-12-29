from random import randint, choice
from math import sqrt, gcd

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
    # Order of prime cyclic group is p - 1 as it has p - 1 elements in group
    q = p - 1
    #Get generator base
    g = []
    base = findGeneratorBase(q)
    # find all coprimes to p - 1 (when divisor of p - 1 and number is only 1 then number is coprime)
    for coprime in range(1, q):
        if gcd(coprime, q) == 1:
            g.append(pow(base, coprime, p)) # every number base^coprime % prime is generator 
    # Return: group, order, generator
    return (p, q, choice(g)) 

def findGeneratorBase(elements):
    # Start from 2 as 1 cannot be generator base
    base = 2
    testBase = []
    # base^element % prime must give unique numbers for all elements
    while True:
        for element in range (1, elements):
            testBase.append(pow(base, element, elements + 1))
        # if numbers are unique then return base of generators else check another one
        if len(testBase) == len(set(testBase)):
            return base 
        else:
            base += 1
            testBase.clear()

def generateKeys(p, q, g):
    x = randint(1, q - 1) # Private Key
    h = pow(g, x)
    publicKey = (p, q, g, h)
    privateKey = x
    return (publicKey, privateKey)

def encryption(message, publicKey):
    y = randint(1, publicKey[1] - 1) # 1 .. q - 1
    s = pow(publicKey[3], y) # h^y
    c1 = pow(publicKey[2], y) # g^y
    c2 = message ^ s
    return (c1, c2)

def decryption(c1, c2, privateKey, group):
    s = pow(c1, privateKey)
    # compute inverse
    inverse = pow(s, group - 2, group)
    #compute m
    m = c2 ^ inverse
    return m

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
        (publicKey, privateKey) = generateKeys(group, order, generator)
        (c1, c2) = encryption(43, publicKey)
        message = decryption(c1, c2, privateKey, group)
        print(message)

if __name__ == "__main__":
    main()