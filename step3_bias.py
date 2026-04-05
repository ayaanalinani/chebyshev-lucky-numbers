import numpy as np
import time

print("Loading sequences...")
lucky = np.loadtxt("lucky_numbers.txt", dtype=np.int64)
primes = np.loadtxt("primes.txt", dtype=np.int64)
print(f"Loaded {len(lucky):,} lucky numbers and {len(primes):,} primes.")

moduli = {
    4:  (3, 1),
    6:  (5, 1),
    10: (3, 1),
    12: (7, 1),
}

def compute_bias(seq, mod, a, b):
    seq = seq[seq % mod != 0]  # remove multiples
    res = seq % mod
    in_a = (res == a).astype(np.int8)
    in_b = (res == b).astype(np.int8)

    # Running difference: count(a) - count(b)
    diff = np.cumsum(in_a.astype(np.int64) - in_b.astype(np.int64))

    # Natural density: fraction of steps where a leads
    natural = np.sum(diff > 0) / len(diff)

    # Logarithmic density: weight each step by 1/n
    indices = np.arange(1, len(diff) + 1, dtype=np.float64)
    weights = 1.0 / indices
    log_num = np.sum(weights[diff > 0])
    log_den = np.sum(weights)
    log_density = log_num / log_den

    final_diff = diff[-1]
    max_lead = diff.max()
    min_lead = diff.min()

    return natural, log_density, final_diff, max_lead, min_lead, diff

print("\n" + "="*65)
print(f"{'':>10} {'Natural Density':>16} {'Log Density':>13}")
print(f"{'Modulus':>10} {'Lucky':>8} {'Primes':>8} {'Lucky':>7} {'Primes':>6}")
print("="*65)

for mod, (a, b) in moduli.items():
    ln, ll, lf, lmax, lmin, _ = compute_bias(lucky, mod, a, b)
    pn, pl, pf, pmax, pmin, _ = compute_bias(primes, mod, a, b)
    print(f"mod {mod:>2} ({a},{b})  {ln:>8.4f}  {pn:>8.4f}  {ll:>7.4f}  {pl:>6.4f}")

print("="*65)
print("\nDone.")
