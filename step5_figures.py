import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Loading sequences...")
lucky = np.loadtxt("lucky_numbers.txt", dtype=np.int64)
primes = np.loadtxt("primes.txt", dtype=np.int64)

moduli = {4: (3,1), 6: (5,1), 10: (3,1), 12: (7,1)}

def get_diff(seq, mod, a, b):
    s = seq[seq % mod != 0]
    r = s % mod
    d = np.cumsum((r==a).astype(np.int64) - (r==b).astype(np.int64))
    return d

def get_log_density(seq, mod, a, b):
    s = seq[seq % mod != 0]
    r = s % mod
    d = np.cumsum((r==a).astype(np.int64) - (r==b).astype(np.int64))
    w = 1.0 / np.arange(1, len(d)+1)
    return np.cumsum(w * (d>0)) / np.cumsum(w)

natural_lucky = {4:7.900, 6:0.000, 10:98.313, 12:28.346}
natural_primes = {4:99.947, 6:99.998, 10:99.472, 12:99.999}
log_lucky  = {4:39.239, 6:0.000, 10:48.304, 12:45.730}
log_primes = {4:88.749, 6:83.488, 10:89.445, 12:84.430}

# ── Figure 1: Running difference plots ──────────────────────────
print("Figure 1...")
fig, axes = plt.subplots(4, 2, figsize=(14, 18))
fig.suptitle("Running Difference $D(x)$ for Lucky Numbers and Primes\nAcross Four Moduli (N = 10,000,000)",
             fontsize=14, fontweight='bold', y=0.98)

for row, (mod, (a, b)) in enumerate(moduli.items()):
    for col, (seq, label, color) in enumerate([
        (lucky, "Lucky Numbers", "#2166ac"),
        (primes, "Primes", "#d6604d")
    ]):
        ax = axes[row, col]
        d = get_diff(seq, mod, a, b)
        x = np.linspace(0, 1, len(d))
        ax.plot(x, d, color=color, linewidth=0.6, alpha=0.9)
        ax.fill_between(x, d, 0,
                        where=(d > 0), color=color, alpha=0.25)
        ax.fill_between(x, d, 0,
                        where=(d < 0), color='gray', alpha=0.20)
        ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
        ax.set_title(f"{label} — mod {mod} (class {a} vs {b})", fontsize=10)
        ax.set_xlabel("Normalized index (0 to N)", fontsize=8)
        ax.set_ylabel("$D(x)$", fontsize=9)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("figure1.png", dpi=200, bbox_inches='tight')
plt.close()
print("  Saved figure1.png")

# ── Figure 2: Natural density bar chart ─────────────────────────
print("Figure 2...")
fig, ax = plt.subplots(figsize=(9, 5))
mods = [4, 6, 10, 12]
x = np.arange(len(mods))
w = 0.35
bl = ax.bar(x - w/2, [natural_lucky[m] for m in mods], w,
            label='Lucky Numbers', color='#2166ac', alpha=0.85)
bp = ax.bar(x + w/2, [natural_primes[m] for m in mods], w,
            label='Primes', color='#d6604d', alpha=0.85)
ax.set_xlabel("Modulus", fontsize=12)
ax.set_ylabel("Natural Bias Density (%)", fontsize=12)
ax.set_title("Natural Bias Density: Lucky Numbers vs Primes\n(Favored Class Leads, N = 10,000,000)",
             fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([f"mod {m}\n(class {moduli[m][0]} vs {moduli[m][1]})" for m in mods])
ax.set_ylim(0, 110)
ax.axhline(50, color='gray', linestyle=':', linewidth=1, label='50% (no bias)')
ax.legend(fontsize=11)
for bar in bl:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
            f"{bar.get_height():.1f}%", ha='center', va='bottom', fontsize=9, color='#2166ac')
for bar in bp:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
            f"{bar.get_height():.1f}%", ha='center', va='bottom', fontsize=9, color='#d6604d')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("figure2.png", dpi=200, bbox_inches='tight')
plt.close()
print("  Saved figure2.png")

# ── Figure 3: Residue class distribution ────────────────────────
print("Figure 3...")
fig, axes = plt.subplots(2, 4, figsize=(16, 7))
fig.suptitle("Residue Class Distributions (N = 10,000,000)", fontsize=13, fontweight='bold')

for col, (mod, (a, b)) in enumerate(moduli.items()):
    for row, (seq, label, color) in enumerate([
        (lucky, "Lucky Numbers", "#2166ac"),
        (primes, "Primes", "#d6604d")
    ]):
        ax = axes[row, col]
        s = seq[seq % mod != 0]
        classes = sorted(set(np.arange(mod).tolist()) - {0})
        counts = [np.sum(s % mod == c) for c in classes]
        bars = ax.bar([str(c) for c in classes], counts, color=color, alpha=0.75)
        for bar, c in zip(bars, classes):
            if c in (a, b):
                bar.set_edgecolor('black')
                bar.set_linewidth(2)
        ax.set_title(f"{label}\nmod {mod}", fontsize=9)
        ax.set_xlabel("Residue class", fontsize=8)
        ax.set_ylabel("Count", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("figure3.png", dpi=200, bbox_inches='tight')
plt.close()
print("  Saved figure3.png")

# ── Figure 4: Logarithmic density comparison ────────────────────
print("Figure 4...")
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(mods))
bl = ax.bar(x - w/2, [log_lucky[m] for m in mods], w,
            label='Lucky Numbers', color='#2166ac', alpha=0.85)
bp = ax.bar(x + w/2, [log_primes[m] for m in mods], w,
            label='Primes', color='#d6604d', alpha=0.85)
ax.set_xlabel("Modulus", fontsize=12)
ax.set_ylabel("Logarithmic Bias Density (%)", fontsize=12)
ax.set_title("Logarithmic Bias Density: Lucky Numbers vs Primes\n(N = 10,000,000)",
             fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([f"mod {m}\n(class {moduli[m][0]} vs {moduli[m][1]})" for m in mods])
ax.set_ylim(0, 110)
ax.axhline(50, color='gray', linestyle=':', linewidth=1, label='50% (no bias)')
ax.legend(fontsize=11)
for bar in bl:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
            f"{bar.get_height():.1f}%", ha='center', va='bottom', fontsize=9, color='#2166ac')
for bar in bp:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
            f"{bar.get_height():.1f}%", ha='center', va='bottom', fontsize=9, color='#d6604d')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("figure4.png", dpi=200, bbox_inches='tight')
plt.close()
print("  Saved figure4.png")

# ── Figure 5: Log-scale running difference ──────────────────────
print("Figure 5...")
fig, axes = plt.subplots(4, 2, figsize=(14, 18))
fig.suptitle("Log-Scale Running Difference $|D(x)|$ (N = 10,000,000)\nSign shown by color: blue = favored class leads, gray = trails",
             fontsize=13, fontweight='bold', y=0.98)

for row, (mod, (a, b)) in enumerate(moduli.items()):
    for col, (seq, label, color) in enumerate([
        (lucky, "Lucky Numbers", "#2166ac"),
        (primes, "Primes", "#d6604d")
    ]):
        ax = axes[row, col]
        d = get_diff(seq, mod, a, b)
        x = np.arange(1, len(d)+1)
        pos = d > 0
        neg = d < 0
        if pos.any():
            ax.scatter(x[pos], np.abs(d[pos]), s=0.05, color=color, alpha=0.5, label=f"class {a} leads")
        if neg.any():
            ax.scatter(x[neg], np.abs(d[neg]), s=0.05, color='gray', alpha=0.4, label=f"class {b} leads")
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title(f"{label} — mod {mod} (class {a} vs {b})", fontsize=10)
        ax.set_xlabel("n (log scale)", fontsize=8)
        ax.set_ylabel("$|D(n)|$ (log scale)", fontsize=9)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3, which='both')
        ax.legend(fontsize=7, markerscale=8)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("figure5.png", dpi=200, bbox_inches='tight')
plt.close()
print("  Saved figure5.png")

print("\nAll 5 figures saved successfully.")
