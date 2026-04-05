# chebyshev-lucky-numbers
Computational investigation of Chebyshev-type bias in the modular distribution of lucky numbers
# Chebyshev-Type Bias in Lucky Numbers

**Author:** Ayaan Alinani, Walter L. Sickles High School, Tampa, Florida

## Overview
This repository contains all code and figures for the paper:
"Chebyshev-Type Bias in the Modular Distribution of Lucky Numbers: 
A Computational Investigation"

## Files
- step1_lucky_numbers.py — Generates lucky numbers to 10,000,000
- step2_primes.py — Generates primes to 10,000,000
- step3_bias.py — Computes natural and logarithmic bias density
- step4_stats.py — Full statistical analysis
- step5_figures.py — Generates all 5 publication figures

## Requirements
Python 3, NumPy, Matplotlib

## Results Summary
Lucky numbers do not exhibit Chebyshev bias. For moduli 4 and 12 
they show reverse bias. For modulus 6 there is complete structural 
exclusion of class 5. For modulus 10 natural density agrees with 
primes but logarithmic density does not.

## Reproducibility
Run scripts in order (step1 through step5). Each script saves 
output to disk for use by subsequent scripts.
