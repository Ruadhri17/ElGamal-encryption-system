from random import randint, getrandbits, randrange

def millerRabinTest(nr, nrOfTimes):
    r = 0 
    s = nr - 1

    # Look for r (r > 0) until the
    # following equation is true: nr = 2^d * r + 1
    while s % 2 == 0:
        r += 1
        s //= 2

    # iterate nrOfTimes times
    for i in range(nrOfTimes):
        # x = a^s % nr
        x = pow(randrange(2, nr - 1), s, nr)

        # continue if x is 1 or nr - 1
        if x == 1 or x == nr - 1:
            continue

        # iterate r - 1 times
        for i in range(r - 1):
            # x = x * x % nr
            x = pow(x, 2, nr)

            # break if x reach nr - 1
            if x == nr - 1:
                break
        else:
            return False
    return True

def fermatPrimalityTest(nr, nrOfTimes):
    # iterate nrOfTimes times
    for i in range(nrOfTimes):
        # Fermat's little theorem says that for every a (that 1 < a < nr-1)
        # flowing equation is true: a^(nr-1) % nr = 1
        if pow(randint(2, nr - 2), nr - 1, nr) != 1:
            return False
    return True

def choosePrime(nrOfBits):
    # true until find prime number
    while True:
        primeCandidate = getrandbits(nrOfBits)
        # check if even number
        if primeCandidate % 2 == 0:
            continue
        # make 100 fermat tests 
        if not fermatPrimalityTest(primeCandidate, 100):
            continue
        # make 100 miller-rabin tests
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
    # choose random integer which will be treated as private key and used for h calculation 
    x = randint(2, q - 1) 
    # calculate h equal g^x mod p, will be used for encryption
    h = pow(g, x, p) 
    publicKey = (p, q, g, h)
    privateKey = x
    return (publicKey, privateKey)

def encryption(messageBlocks, publicKey):
    p = publicKey[0] # Group (prime number)
    q = publicKey[1] # order
    g = publicKey[2] # generator
    h = publicKey[3] 
    encryptedBlocks = []
    for block in messageBlocks:
        encryptedPairs = []
        # randomly selected y for future calculations
        y = randint(2, q - 1)
        # compute shared secret
        s = pow(h, y, p)
        # first part of cipher text
        c1 = pow(g, y, p)
        for sign in block:
            #second part of cipher text
            c2 = (sign * s ) % p
            # keep both parts as a pair for decryption 
            encryptedPairs.append([c1,c2])
        #separate each block pairs 
        encryptedBlocks.append(encryptedPairs)
    return encryptedBlocks

def decryption(encryptedBlocks, privateKey, group):
    messageBlocks = []
    for encryptedBlock in encryptedBlocks:
        block = []
        for pair in encryptedBlock:
            # compute inverse of shared secret as c1^(-x) mod p 
            s = pow(pair[0], -1 * privateKey, group)
            # decrypt message: c^2 * s mod p 
            m = (pair[1]* s) % group
            # add message to block
            block.append(m)
        # when whole block is decrypted, add to the rest of message blocks    
        messageBlocks.append(block)
    return messageBlocks

def convertMsgToBlocks(msg):
    blocks = []
    for char in msg:
        # convert char to nr
        blocks.append(ord(char))
    messageBlocks = [blocks[i:i+16] for i in range (0, len(blocks), 16)]
    return messageBlocks

def convertBlocksToMsg(messageBlocks):
    # placeholder for msg block
    oneMessageBlock = []

    # placeholder for msg
    msg = ''

    for block in messageBlocks:
        oneMessageBlock += block

    for element in oneMessageBlock:
        # convert nr to char
        msg += chr(element)
    return msg
    
def writeEncryptedMessage(encryptedBlocks):
    # open ciphertext with write flag
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
    writeEncryptedMessage(encryptedBlocks)
    # decrypt message blocks with private key 
    messageBlocks = decryption(encryptedBlocks, privateKey, group)
    # convert messsage block to one message
    msg = convertBlocksToMsg(messageBlocks)
    # write decrypted messsage to file 
    open("decryptedtext.txt", "w").write(msg)

if __name__ == "__main__":
    main()