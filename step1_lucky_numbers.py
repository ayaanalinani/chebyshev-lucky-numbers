import numpy as np
import time

def generate_lucky_numbers(limit):
    sieve = np.arange(1, limit + 1, 2, dtype=np.int32)
    idx = 1
    while idx < len(sieve):
        step = int(sieve[idx])
        if step > len(sieve):
            break
        mask = np.ones(len(sieve), dtype=bool)
        mask[step - 1::step] = False
        sieve = sieve[mask]
        idx += 1
    return sieve

print("Generating lucky numbers up to 10,000,000...")
start = time.time()
lucky = generate_lucky_numbers(10_000_000)
elapsed = time.time() - start

print(f"Done in {elapsed:.1f} seconds.")
print(f"Count: {len(lucky):,}")
print(f"First 15: {lucky[:15].tolist()}")
print(f"Last 5:   {lucky[-5:].tolist()}")

np.savetxt("lucky_numbers.txt", lucky, fmt="%d")
print("Saved to lucky_numbers.txt")
