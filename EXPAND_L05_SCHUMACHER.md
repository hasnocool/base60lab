## EXPAND

**LEAD: Schumacher 2016 (arXiv:1608.06928v4) — Exact convergent formulas for 3-smooth, 5-smooth, 7-smooth counting functions** — WHY: Provides rapidly convergent exact formulas for counting smooth numbers, directly applicable to predicting optimal FFT sizes for base-12 (2^a·3^b = 3-smooth) and base-60 (2^a·3^b·5^c = 5-smooth) FFT benchmarking. The formulas give exact counts, density estimates, and enable optimal size selection near any target length. — ANGLE: Implement exact counting/enumeration algorithms; derive asymptotic density for Experiment D FFT size prediction; provide inverse lookup (k-th smooth number) for benchmark planning.

**DEAD END: None** — Paper fully delivers on its claims; all formulas verified against published tables; practical Python implementation created and tested.

---

### Key Findings for Experiment D

| Aspect | 3-smooth (Base-12) | 5-smooth (Base-60) | 7-smooth (Base-420) |
|--------|-------------------|-------------------|-------------------|
| **Counting function** | N_{2,3}(x) | N_{2,3,5}(x) | N_{2,3,5,7}(x) |
| **Leading asymptotic** | ½ log(2x)log(3x)/(log2 log3) | √3 log³x/(6 log2 log3 log5) | log⁴x/(24 log2 log3 log5 log7) |
| **Count at 10⁶** | 142 | 507 | 1,273 |
| **Count at 10⁷** | 190 | 768 | 2,155 |
| **Avg gap at 10⁶** | ~7,042 | ~1,972 | ~786 |
| **Avg gap at 10⁷** | ~52,632 | ~13,021 | ~4,640 |

### Practical Application

**Finding optimal FFT size near target T:**
```python
# Base-12 (radix-2,3): 3-smooth numbers
candidates = find_optimal_3smooth_near(T, radius=T//100)

# Base-60 (radix-2,3,5): 5-smooth numbers  
candidates = find_optimal_5smooth_near(T, radius=T//100)
```

**Density estimation for benchmark planning:**
- At N=10⁶: 507 valid base-60 FFT sizes exist → dense coverage
- At N=10⁷: 768 valid base-60 FFT sizes → avg gap ~13k
- Use `density_analysis(T)` to estimate candidate pool size

**Inverse lookup (k-th smooth number):**
```python
# Find 1000th base-60 FFT size
size_1000 = find_kth_5smooth(1000)  # Returns 51,200,000
```

### Implementation Artifacts Created
1. `/home/hyperion/Projects/Base60Research/schumacher_2016_summary.md` — Full formula extraction
2. `/home/hyperion/Projects/Base60Research/smooth_fft_sizes.py` — Production-ready Python module with exact counting, enumeration, optimal selection, and inverse lookup

All paper formulas verified against Tables 1, 3, 4 — exact matches.