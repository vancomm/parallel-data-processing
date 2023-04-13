import math
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("n")
args = parser.parse_args()

n = int(args.n)
sqrt_n = math.sqrt(n)

arr = np.full(n, True)
k = 2

while k <= sqrt_n:
    for i in range(0, n, k):
        arr[i] = False
    k += 1

primes = [i for i in range(n) if arr[i]]

print(primes)
