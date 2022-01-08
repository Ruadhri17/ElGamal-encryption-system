from random import randint, getrandbits, randrange

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
    #the prime divisors of p-1 are 2 and (p-1)/2 because p = 2x + 1 where x is a prime
    p1 = 2
    p2 = (p - 1) // p1
    #test random g's until one is found that is a primitive root mod p
    while True:
        g = randint(2, p - 1)
        #g is a primitive root if for all prime factors of p-1, p[i]
        #g^((p-1)/p[i]) (mod p) is not congruent to 1
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

def encryption(messageBlocks, publicKey):
    encryptedBlocks = []
    for block in messageBlocks:
        encryptedPairs = []
        y = randint(2, publicKey[1] - 1)
        s = pow(publicKey[3], y, publicKey[0])
        c1 = pow(publicKey[2], y, publicKey[0])
        for element in block:
            c2 = (element * s ) % publicKey[0]
            encryptedPairs.append([c1,c2])
        encryptedBlocks.append(encryptedPairs)
    return encryptedBlocks

def decryption(encryptedBlocks, privateKey, group):
    messageBlocks = []
    for encryptedBlock in encryptedBlocks:
        block = []
        for pair in encryptedBlock:
            s = pow(pair[0], group - 1 - privateKey, group)
            m = (pair[1]* s) % group
            block.append(m)
        messageBlocks.append(block)
    return messageBlocks

def convertMsgToBlocks(msg):
    blocks = []
    for char in msg:
        blocks.append(ord(char))
    messageBlocks = [blocks[i:i+16] for i in range (0, len(blocks), 16)]
    return messageBlocks

def convertBlocksToMsg(messageBlocks):
    oneMessageBlock = []
    msg = ''
    for block in messageBlocks:
        oneMessageBlock += block
    for element in oneMessageBlock:
        msg += chr(element)
    return msg
    
def writeEnryptedMessage(encryptedBlocks):
    f = open("ciphertext.txt", "w")
    for block in encryptedBlocks:
        for element in block:
            f.write(str(element[0]) + ' ' + str(element[1]) + ' ')
    f.close
    
def main():
    
    # read plain text
    msg = open("plaintext.txt", "r").read()
    # convert into several blocks
    msgBlocks = convertMsgToBlocks(msg)
    # choose prime number for cyclic group, number of bits can be chosen by user
    prime = choosePrime(1024)
    print("Generated Prime: ", prime)
    # find order and generator of given cyclic group
    (group , order , generator) = cyclicGroupDescription(prime)
    print("Chosen generator: ", generator)
    # generate public and private keys 
    (publicKey, privateKey) = generateKeys(group, order, generator)
    # encrypt message blocks with public key
    encryptedBlocks = encryption(msgBlocks, publicKey)
    # write encrypted message to file
    writeEnryptedMessage(encryptedBlocks)
    # decrypt message blocks with private key 
    messageBlocks = decryption(encryptedBlocks, privateKey, group)
    # convert messsage block to one message
    msg = convertBlocksToMsg(messageBlocks)
    # write decrypted messsage to file 
    open("decryptedtext.txt", "w").write(msg)

if __name__ == "__main__":
    main()