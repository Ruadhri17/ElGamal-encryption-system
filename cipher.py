from random import randint, choice, getrandbits, randrange
from math import sqrt, gcd

def millerRabinTest(nr, nrOfTimes):
    if nr % 2 == 0:
        return False

    r, s = 0, nr - 1

    while s % 2 == 0:
        r += 1
        s //= 2

    for i in range(nrOfTimes):
        x = pow(randrange(2, nr - 1), s, nr)

        if x == 1 or x == nr - 1:
            continue

        for i in range(r - 1):
            x = pow(x, 2, nr)
            if x == nr - 1:
                break
        else:
            return False
    return True

def fermatPrimalityTest(nr, nrOfTimes):
    for i in range(nrOfTimes):
        if pow(randint(2, nr - 2), nr - 1, nr) != 1:
            return False
    return True

def choosePrime(nrOfBits):
    while True:
        primeCandidate = getrandbits(nrOfBits)
        if primeCandidate % 2 == 0:
            continue
        if not fermatPrimalityTest(primeCandidate, 100):
            continue
        if not millerRabinTest(primeCandidate, 100):
            continue
        return primeCandidate

def findPrimitiveRoot(p):
    if p == 2:
        return 1

    p1 = 2
    p2 = (p - 1) // p1

    while True:
        g = randint(2, p - 1)
        if not (pow(g, (p - 1) // p1, p) == 1):
            if not (pow(g, (p - 1) // p2, p) == 1):
                return g

def cyclicGroupDescription(p):
    # Order of prime cyclic group is p - 1 as it has p - 1 elements in group
    q = p - 1
    # Get generator which is primitive root of prime number
    g = findPrimitiveRoot(p)
    return (p, q, g)

def generateKeys(p, q, g):
    x = randint(2, q - 1) # Private Key
    h = pow(g, x, p)
    publicKey = (p, q, g, h)
    privateKey = x
    return (publicKey, privateKey)

def encryption(message, publicKey, group):
    y = randint(2, publicKey[1] - 1)
    s = pow(publicKey[3], y, publicKey[0])
    c1 = pow(publicKey[2], y, publicKey[0])
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
    print("Generated Prime: ", prime)

    (group , order , generator) = cyclicGroupDescription(prime)
    print("Chosen generator: ", generator)

    (publicKey, privateKey) = generateKeys(group, order, generator)

    (c1, c2) = encryption(1225429105280, publicKey, group)

    message = decryption(c1, c2, privateKey, group)
    print(message)

if __name__ == "__main__":
    main()