import numpy as np
import time

def sieve_of_eratosthenes(limit):
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return np.where(is_prime)[0].astype(np.int32)

print("Generating primes up to 10,000,000...")
start = time.time()
primes = sieve_of_eratosthenes(10_000_000)
elapsed = time.time() - start

print(f"Done in {elapsed:.1f} seconds.")
print(f"Count: {len(primes):,}")
print(f"First 15: {primes[:15].tolist()}")
print(f"Last 5:   {primes[-5:].tolist()}")

np.savetxt("primes.txt", primes, fmt="%d")
print("Saved to primes.txt")
