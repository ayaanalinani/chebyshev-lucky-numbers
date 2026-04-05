import numpy as np

print("Loading sequences...")
lucky = np.loadtxt("lucky_numbers.txt", dtype=np.int64)
primes = np.loadtxt("primes.txt", dtype=np.int64)

moduli = {
    4:  (3, 1),
    6:  (5, 1),
    10: (3, 1),
    12: (7, 1),
}

def compute_full_stats(seq, mod, a, b, label):
    seq_filtered = seq[seq % mod != 0]
    res = seq_filtered % mod
    count_a = np.sum(res == a)
    count_b = np.sum(res == b)
    diff = np.cumsum((res == a).astype(np.int64) - (res == b).astype(np.int64))
    natural = np.sum(diff > 0) / len(diff)
    indices = np.arange(1, len(diff) + 1, dtype=np.float64)
    weights = 1.0 / indices
    log_density = np.sum(weights[diff > 0]) / np.sum(weights)
    final = diff[-1]
    mx = diff.max()
    mn = diff.min()

    print(f"  [{label}]")
    print(f"    Count in class {a}: {count_a:,}")
    print(f"    Count in class {b}: {count_b:,}")
    print(f"    Natural bias density (class {a} leads): {natural:.6f} ({natural*100:.3f}%)")
    print(f"    Logarithmic bias density:               {log_density:.6f} ({log_density*100:.3f}%)")
    print(f"    Final running difference:               {final:+,}")
    print(f"    Maximum lead (class {a}):               {mx:+,}")
    print(f"    Minimum lead (class {a}):               {mn:+,}")

for mod, (a, b) in moduli.items():
    print(f"\n{'='*55}")
    print(f"  MODULUS {mod}  —  comparing class {a} vs class {b}")
    print(f"{'='*55}")
    compute_full_stats(lucky, mod, a, b, "Lucky Numbers")
    print()
    compute_full_stats(primes, mod, a, b, "Primes")

print("\nDone.")
