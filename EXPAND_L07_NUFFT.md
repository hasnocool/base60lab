# EXPANSION LEAD L-07: Mixed-Radix Tensor for NUFFT/MRI

**Paper**: Lin et al., "Memory reduced non-Cartesian MRI encoding using the mixed-radix tensor product on CPU and GPU", arXiv:1903.08365v2 (2019, v1 March 2019, v2 May 2020)

---

## KEY FINDINGS

### 1. What the Paper Actually Does

The paper proposes a **tensor decomposition method for the NUFFT interpolator** in multi-dimensional non-Cartesian MRI reconstruction. The "mixed-radix" refers to **how dimensions are grouped during partial precomputation of the interpolator**, not to prime factorization of FFT sizes.

**Core insight**: The multi-dimensional NUFFT interpolator is a rank-1 tensor (outer product of 1D interpolators). Instead of fully precomputing the D-dimensional interpolator (storage ∝ M∏J_d[d]), they store 1D components (storage ∝ M∑J_d[d]) and reconstruct at runtime via tensor product on the accelerator.

### 2. Memory Savings (The 88% / 62% Numbers)

From **Table II** (3D MRI, 256³, 262K samples, 2× oversampling, 6×6×6 interpolator):

| Configuration | Total Storage | Memory Saving |
|--------------|---------------|---------------|
| radix-3 (full precompute) | 27,061 MB | 0% (baseline) |
| radix-2-1 | 6,114 MB | **77.4%** |
| radix-1-1-1 | 3,234 MB | **88.1%** |

From **Table III** (2D+time CINE MRI, 192²×29, 6 coils, batched 3D):

| Configuration | Total Storage | Memory Saving |
|--------------|---------------|---------------|
| radix-4 | 606 MB | 0% (baseline) |
| radix-1-1-1-1 | 351 MB | **42.1%** |
| radix-1-1-1 (batched) | 228 MB | **62.4%** |

### 3. The "Mixed-Radix" Meaning in This Paper

The paper defines **radix** as the **number of dimensions grouped together in precomputation**:

- **radix-D** = full precomputation (all D dimensions combined) — largest storage, fastest runtime
- **radix-1** = fully decomposed (each dimension separate) — smallest storage, more runtime work
- **radix-2-1** = group 2 dimensions, leave 1 separate (e.g., for 3D: combine x,y, keep z separate)
- **radix-3-1** = group 3 dimensions, leave 1 separate (for 4D problems)

This is a **tree-like recursive precomputation** where subsets of dimensions are collapsed during planning, then expanded at runtime on the GPU/CPU.

---

## RELEVANCE TO BASE-60 SMOOTH FFT SIZES

### Direct Connection: **None**

The paper **does not mention**:
- base-60, sexagesimal, 60-smooth numbers
- 5-smooth numbers (2^a 3^b 5^c) as FFT size optimization
- Prime factorization of FFT grid sizes for mixed-radix Cooley-Tukey

### Indirect Connection: **The FFT Inside NUFFT**

The NUFFT algorithm (Eq 4-5) uses an **oversampled FFT** (F matrix) on a Cartesian grid:
- 3D example: 256³ image → 512³ oversampled grid (2× oversampling)
- 2D example: 192² image → 384² oversampled grid (2× oversampling)

**These FFT sizes happen to be powers of 2** (512 = 2⁹, 384 = 2⁷×3). If one chose **5-smooth oversampled grid sizes** (2^a 3^b 5^c), the internal FFT could use mixed-radix Cooley-Tukey (as implemented in GSL, FFTW, sangi, OxiFFT, etc.) instead of Bluestein/power-of-2-only FFTs.

### What Would Connect Them

To make base-60 smooth FFT sizes relevant to this paper's method:
1. Choose oversampled grid dimensions as **5-smooth numbers** (2^a 3^b 5^c) instead of powers of 2
2. The internal FFT (F matrix in Eq 5) would then use mixed-radix FFT
3. The paper's tensor decomposition of the interpolator (V matrices) is **orthogonal** to this — it reduces interpolator storage regardless of FFT size

**Key point**: The paper's 88%/62% savings come from **interpolator tensor decomposition**, not from FFT size selection. The FFT size is a separate optimization axis.

---

## ALGORITHM DETAILS

### Tensor Form of NUFFT (Eq 5)

For 3D:
```
Y = X ×₁ W_x ×₂ W_y ×₃ W_z ×₁ F_x ×₂ F_y ×₃ F_z ×₁ V_x ×₂ V_y ×₃ V_z
```

Where:
- X = image tensor (N_x × N_y × N_z)
- W_d = diagonal scaling factors (roll-off)
- F_d = oversampled FFT matrices (K_d × N_d)
- V_d = interpolator matrices (M × K_d) — sparse, rank-1 in tensor sense

### Radix-1 Interpolation (Algorithm 1)

Stores per-dimension:
- `kindx[m, sum(J_d)]` — k-space indices (1D per dimension)
- `udata[m, sum(J_d)]` — interpolator values (1D per dimension)
- `meshindex[prod(J_d) × D]` — multi-dimensional index map

Runtime: Each thread reads meshindex, computes multi-D index by multiplying 1D components, applies to k-space data.

### Mixed-Radix Precomputation (Fig 3)

Recursive grouping:
```
3D: (0,1,2) → (01,2) [radix-2-1] → (012) [radix-3]
4D: (0,1,2,3) → (012,3) [radix-3-1] → (0123) [radix-4]
```

Each grouping increases precomputation (more storage) but reduces runtime work.

---

## CONCLUSION FOR BASE-60 RESEARCH

### What This Paper Provides
- Proven method to reduce NUFFT interpolator storage by 62-88% via tensor decomposition
- Working GPU/CPU implementation (PyNUFFT with OpenCL/CUDA backends)
- Validation on clinical cardiac MRI data

### What It Does NOT Provide
- Any analysis of FFT size selection for smooth numbers
- Base-60 or 5-smooth number theory
- Connection between tensor rank and number-theoretic smoothness

### Research Angle for Base-60
The paper's method **could be combined** with smooth-FFT-size selection:
1. Use tensor decomposition (this paper) for interpolator storage reduction
2. Choose oversampled grid sizes as **5-smooth (base-60 smooth) numbers** for optimal mixed-radix FFT
3. The two optimizations are **independent and composable**

This is a **systems-level integration opportunity**, not a theoretical connection in the paper itself.

---

## EXPAND
- LEAD: Mixed-radix tensor interpolator decomposition (Lin et al. 1903.08365) — WHY: Achieves 88% (3D) / 62% (2D) NUFFT interpolator memory reduction via tensor rank-1 decomposition; validated on clinical MRI — ANGLE: Combine with 5-smooth oversampled grid sizes for FFT to get compound optimization; investigate if tensor decomposition patterns align with base-60 factorization structure
- DEAD END: Direct "base-60 NUFFT" or "sexagesimal MRI" papers — No papers found connecting base-60 number theory to NUFFT or MRI reconstruction