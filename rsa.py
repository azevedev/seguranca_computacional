# https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation

import base64
from math import gcd
import random
import numpy as np

def findD(e: int, phi: int) -> int:
    i = 1;
    x = 0;
    while (True) :
        if (e * i % phi == 1) :
            return i
        i+=1

# From https://stackoverflow.com/a/56994391  (fast way to get random prime numbers)
def getRandomPrimeInteger(bounds):
    for i in range(bounds.__len__()-1):
        if bounds[i + 1] > bounds[i]:
            x = bounds[i] + np.random.randint(bounds[i+1]-bounds[i])
            if isPrime(x):
                return x

        else:
            if isPrime(bounds[i]):
                return bounds[i]

        if isPrime(bounds[i + 1]):
            return bounds[i + 1]

    newBounds = [0 for i in range(2*bounds.__len__() - 1)]
    newBounds[0] = bounds[0]
    for i in range(1, bounds.__len__()):
        newBounds[2*i-1] = int((bounds[i-1] + bounds[i])/2)
        newBounds[2*i] = bounds[i]

    return getRandomPrimeInteger(newBounds)

def isPrime(x):
    count = 0
    for i in range(int(x/2)):
        if x % (i+1) == 0:
            count = count+1
    return count == 1

def generate_keys():
  p = getRandomPrimeInteger([1, 1024])
  q = getRandomPrimeInteger([1, 1024])
  n = p * q

  phi = (p - 1) * (q - 1)
  
  # getting one of the coprime numbers
  # so that e and phi are coprime
  e = int(n / 2)
  while e < phi:
    if gcd(e, phi) == 1:
      break
    e += 1

  d = findD(e, phi)

  return n, e, d


number, public_key, private_key = generate_keys()

def encrypt(msg, public_key, number):
    total_len = len(msg)
    enconded = msg.encode('utf-8')
    msg = int.from_bytes(enconded, byteorder='big')
    msg = pow(msg, public_key, number)
    ok = msg.to_bytes(total_len + 1, byteorder='big')
    return ok.hex()
def decrypt(cypher, private_key, number):
    cypher = int.from_bytes(cypher.encode(), byteorder='big')
    result = pow(cypher, private_key, number)
    return result.to_bytes(len(cypher) + 1, byteorder='big')

