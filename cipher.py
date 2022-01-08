from random import randint, choice, getrandbits
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

def millerRabinTestMultiple(nr, nrOfTimes):
    while(nrOfTimes > 0):
        if millerRabinTest(nr) == False:
            return False
        nrOfTimes = nrOfTimes - 1
    return True

def millerRabinTest(nr):
    d = nr - 1
    while (d % 2 == 0):
        d //= 2

    a = 2 + randint(1, nr - 4)

    x = pow(a, d, nr)

    if (x == 1 or x == nr - 1):
        return True

    while (d != nr - 1):
        x = (x * x) % nr
        d *= 2

        if (x == 1):
            return False
        if (x == nr - 1):
            return True

    return False

def fermatPrimalityTest(nr, nrOfTimes):
    for i in range(nrOfTimes):
    
        a = randint(2, nr - 2)

        if pow(a, nr - 1, nr) != 1:
            return False
    return True

def choosePrime(numberOfBits):
    while True:
        primeCandidate = getrandbits(numberOfBits)
        if primeCandidate % 2 == 0:
            continue
        if not fermatPrimalityTest(primeCandidate, 1000):
            continue
        if not millerRabinTestMultiple(primeCandidate, 1000):
            continue
        return primeCandidate
    
def cyclicGroupDescription(p):
    # Order of prime cyclic group is p - 1 as it has p - 1 elements in group
    q = p - 1
    # Get generator base
    g = []
    base = findGeneratorBase(q)
    # Find all coprimes to p - 1 (when divisor of p - 1 and number is only 1 then number is coprime)
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
    x = randint(2, q - 1) # Private Key
    h = pow(g, x, p)
    publicKey = (p, q, g, h)
    privateKey = x
    return (publicKey, privateKey)

def encryption(message, publicKey, group):
    y = randint(2, publicKey[1] - 1) # 2 .. q - 1
    s = pow(publicKey[3], y, publicKey[0]) # h^y
    c1 = pow(publicKey[2], y, publicKey[0]) # g^y
    c2 = (message * s ) % publicKey[0]
    return (c1, c2)

def decryption(c1, c2, privateKey, group):
    s = pow(c1, group - 1 - privateKey, group)
    # Compute inverse
    # inverse = pow(s, group - 2, group)
    # Compute m
    m = (c2 * s) % group
    return m

def main():
    prime = choosePrime(1024)
    print(prime)
    try:
        value = int(input("Choose cyclic group size (enter prime number): "))
    except ValueError:
        print("Input is not valid!")
        return
    if isPrime(value) == False:
        print("Input is not prime number!")
        return
    else:
        (group , order , generator) = cyclicGroupDescription(prime)
        print("Chosen generator: ", generator)

        (publicKey, privateKey) = generateKeys(group, order, generator)

        (c1, c2) = encryption(3000, publicKey, group)

        message = decryption(c1, c2, privateKey, group)
        print(message)

if __name__ == "__main__":
    main()