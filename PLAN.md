# **Base-12 / Base-60 Mathematical Research Programme**



Research proposal

Experimental mathematics



**Objective:** Determine whether base-12 and base-60 representations provide practical advantages for understanding, calculating, visualising and discovering relationships in fractions, geometry, trigonometry, frequency analysis and digital signal processing.

I recommend treating this as an independent research project with reproducible experiments, mathematical proofs, visualisations and performance benchmarks.

One important historical distinction: the Mesopotamian mathematical tradition developed over several periods. The earlier Sumerian numerical traditions and the later Babylonian positional sexagesimal system should not be treated as exactly the same achievement. The sophisticated base-60 positional system is particularly well documented in Babylonian mathematics.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mathshistory.st-andrews.ac.uk\&sz=32)

MacTutor History of Mathematics+1



## **1. The central research hypothesis**

I would establish five primary hypotheses.

| ID | Hypothesis                                                                  | What we're testing                        |
| -- | --------------------------------------------------------------------------- | ----------------------------------------- |
| H1 | Base 12 simplifies fractional relationships                                 | Exact fractions, reciprocals and division |
| H2 | Base 60 simplifies proportional geometry                                    | Angles, rotations and cyclic geometry     |
| H3 | Combined base-12/base-60 representations help reveal periodic relationships | Frequency ratios, harmonics and phase     |
| H4 | Base-12/base-60-friendly sample lengths can be useful in signal processing  | FFT factorisation and performance         |
| H5 | Alternative numerical representations improve mathematical exploration      | Pattern discovery and problem-solving     |

The most important distinction is that these hypotheses don't assume the answers will be positive.

We may find that base 60 is superior for one mathematical task, base 12 for another, and decimal remains better for something else.

That would still be a valuable result.

## **2. First, establish the mathematical foundations**

Before testing anything, we need a consistent way of translating the same numerical quantity between different representations.

**The three primary numerical systems**

# **10**

Decimal

2 × 5

# **12**

Duodecimal

2² × 3

# **60**

Sexagesimal

2² × 3 × 5

**Why these factorisations matter**

- Base 10 naturally terminates fractions with denominator factors 2 and 5.
- Base 12 naturally terminates fractions with denominator factors 2 and 3.
- Base 60 naturally terminates fractions with denominator factors 2, 3 and 5.

This is a mathematical property of positional notation, not a matter of opinion. A rational number has a terminating representation in a given integer base precisely when the prime factors of its reduced denominator all divide that base.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.open.edu\&sz=32)

OpenLearn+1



That gives us our first measurable advantage.

### **The proposed numerical representation engine**

We should build a common mathematics layer that can represent:

- Decimal integers and fractions.
- Duodecimal integers and fractions.
- Sexagesimal positional integers and fractions.
- Exact rational numbers.
- High-precision irrational numbers.
- Angles expressed as degrees, radians and turns.
- Frequencies represented as exact ratios where possible.

Internally, calculations should use exact rational or symbolic mathematics wherever possible. The displayed base is a presentation choice, not the underlying value.

This prevents numerical rounding from creating false patterns.

# **3. Experiment A: Fractions, division and reciprocals**

First experiment

**Question:** Does base 12 or base 60 provide a more useful mathematical language for fractional relationships?

We begin with a controlled collection of fractions.

For example:

\\[ \frac12,\quad \frac13,\quad \frac14,\quad \frac15,\quad \frac16,\quad \frac17,\quad \frac1{12},\quad \frac1{15} \\]

Compare their representations in all three bases.

| Fraction | Base 10  | Base 12   | Base 60 |
| -------- | -------- | --------- | ------- |
| 1/2      | 0.5      | 0.6       | 0;30    |
| 1/3      | 0.333…   | 0.4       | 0;20    |
| 1/4      | 0.25     | 0.3       | 0;15    |
| 1/5      | 0.2      | 0.2497…\* | 0;12    |
| 1/6      | 0.1666…  | 0.2       | 0;10    |
| 1/12     | 0.08333… | 0.1       | 0;5     |

\*In conventional duodecimal digit notation, 1/5 is 0.24972497… (the repeating sequence 2497). For base 12, A and B represent ten and eleven.

**Experiments to perform:**

1. Generate reciprocals for denominators 1–360.
2. Count terminating representations.
3. Measure the repeating period of non-terminating representations.
4. Compare multiplication and division tables.
5. Examine which ratios produce the simplest expressions in each system.

**Success measurement:** Number of terminating fractions, representation length and complexity of recurring sequences.

A particularly interesting extension is investigating whether the simplest representation also makes it easier for a person to perform mental calculations.

# **4. Experiment B: Geometry, circles and trigonometry**

High priority

This is where the relationship between 12, 60 and 360 becomes especially interesting.

A full circle contains 360 degrees:

\\[ 360=6\times60=30\times12 \\]

This gives us two natural ways of dividing a circle:

[Polar Grid In Degrees With Radius 1 | ClipArt ETC](https://images.openai.com/static-rsc-4/VIfByaaVEqSxobsv0UGJZSIK-rbQlxnu3_5EM3bfzArHBYqiHaRp36ufCP-LBX1IrQWJRak6U_sdiKizOQtqL00O3FJ9guJlIBVOv2M9KffApz-Iyo41vp-8YCWF-heQoOlfG2Gdvvkgw0pzy33DxX21-m4v03PV8yj3mDEdFC4?purpose=inline)

**12 divisions**

30° per division

[Tool for dividing a circle into slices? | Community](https://images.openai.com/static-rsc-4/NNAKbnoNFNkOQSJttWDzaqrzHvVuI87GpP3ceEwbF6VU05wu_9RMg-_lf6R2ozcHqLe_X2ctYWXxaZLb2_5a63GDvYM2KgSK8t13eWke9dE8kRWCYsGT54pqEOm-B3xTvjPhyHycZWek1_HWZ5wf0KDA7Q3YJfF8dolNFywX4Xc?purpose=inline)

**60 divisions**

6° per division

We should test whether different angular representations make geometric calculations easier.

### **Tests**

**B1. Circle subdivisions**

Compare 12, 24, 30, 36, 60, 120, 180 and 360 divisions.

**B2. Polygon geometry**

Examine regular polygons, their internal angles, exterior angles, symmetry and chord lengths.

**B3. Trigonometric values**

Investigate familiar values such as:

\\[ \sin(30^\circ),\quad \sin(45^\circ),\quad \sin(60^\circ) \\]

Then investigate angles that don't fall neatly into a 12-part circle.

**B4. Rotation and phase**

Represent rotation as a fraction of a complete turn rather than only degrees or radians.

For example:

\\[ \theta = \frac{1}{3}\text{ turn} \\]

is 120 degrees, or \\(2\pi/3\\) radians.

The key comparison is whether turn-based, dozenal and sexagesimal angle representations help reveal relationships more clearly than decimal-degree representations.

One important control: radians remain a particularly natural mathematical angle measure because they arise directly from the geometry of the unit circle. We should not assume that replacing radians with base 60 improves trigonometric identities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://openstax.org\&sz=32)

OpenStax



# **5. Experiment C: Frequency, harmonics and vibration**

Core research experiment

This is probably the most interesting part of the entire project, particularly because it lets us investigate repeating patterns in physical phenomena.

Frequency is the number of cycles occurring per second. Phase describes the position within a cycle.

We can express phase as a fraction of a complete rotation:

\\[ \phi = ft \pmod 1 \\]

where:

- \\(f\\) is frequency in cycles per second.
- \\(t\\) is elapsed time.
- \\(\phi\\) is the fractional position in a cycle.

The angle equivalent is:

\\[ \theta=2\pi\phi \\]

This gives us an opportunity to investigate phase in three representations:

| Representation        | Complete cycle |
| --------------------- | -------------- |
| Decimal degrees       | 360°           |
| Dozenal divisions     | 12 × 30°       |
| Sexagesimal divisions | 60 × 6°        |
| Radians               | \\(2\pi\\)     |

### **C1. Frequency ratios**

We'll examine relationships such as:

\\[ 1:1,\quad 2:1,\quad 3:2,\quad 4:3,\quad 5:4,\quad 5:3 \\]

These are important because they describe relationships between oscillations.

For example:

- 2:1 means one frequency is twice another.
- 3:2 means one frequency completes three cycles while the other completes two.
- 4:3 means four cycles against three.

We can compare the numerical representations of these ratios and measure how easily their repeating patterns can be understood.

### **C2. Harmonic relationships**

Generate waveforms containing multiple frequencies:

\\[ x(t)= \sin(2\pi ft) +\frac12\sin(4\pi ft) +\frac13\sin(6\pi ft) \\]

This is a simple example of a signal containing a fundamental frequency and its harmonics.

We then investigate:

- Fundamental frequencies.
- Harmonic spacing.
- Phase alignment.
- Amplitude relationships.
- Beat frequencies.
- Periodic repetition.

[What Are Harmonics in Audio? Fundamental and Harmonic Frequencies Explained](https://images.openai.com/static-rsc-4/nTC_jaYpIm3bebJZ81OPWx3bCHBdPmQ05t0y0uLlstb1g9iheUu9utGtBlJIn3R0WzSIc8Il1A8RFwAeqM1m6iD5rvNcEUhpBJ7rODheRWF17uMoXcnglZzY3BWqms10E9a_qfOV7AV_jyY2FGrfrTYcydVxnvRCKG0n1WUs_9g?purpose=inline)

[Interference Patterns on a Water Surface: Wave Superposition Analysis - Physics and Mathematics](https://images.openai.com/static-rsc-4/_XCuNM_VP5Tp4Suc5v4Y3JkMFeQMUgjaY_ldZribfla_Bzy68qIPLlVxTdEqb2s_XjMp3t2va_IK01xEWCTlpXvl-uVDbu6JRYSEQ2ViR9kVev2dR4h5rCOwTNK0HGnTr-s_NOwvSZscaw0QdoujAJbXSh-vccu53ewtyfSGCas?purpose=inline)

[Online Developer's WhizzCave - Projecting Lissajous curves](https://images.openai.com/static-rsc-4/LcrlUGCHT1EdBgHy8dzA-aSBghd3Heuyp2-FqmA74-je895aDVbjHpiM-cdP2QP3JKaShqZtvnhSdxAYv7EaNmbc8jUBOsZ717u4e6ypvevdqGf8sxywlkKHxTwwWuLQ0mPc32seyuIUloCrmWS2bCEukz474Wx4SzNr-F22uPQ?purpose=inline)

7

### **C3. Lissajous figures**

I particularly want to include this experiment.

A Lissajous figure is formed by plotting two oscillations against each other:

\\[ x(t)=\sin(2\pi f_1t) \\]

\\[ y(t)=\sin(2\pi f_2t+\delta) \\]

When the frequency ratio is rational, the resulting figure closes into a repeating pattern.

For example, 3:2 produces a different geometric figure from 5:4.

We should compare ratios whose denominators contain only factors of 2, 3 and 5 against ratios involving primes such as 7, 11 and 13.

**The question:** Do base-12 and base-60 representations help us recognise the relationships between frequency ratios, phase and geometric closure?

### **C4. Musical tuning as a special investigation**

There is an especially interesting modern example of 12-based mathematics: twelve-tone equal temperament.

An octave is divided into twelve equal logarithmic steps.

The frequency ratio of each step is:

\\[ r=2^{1/12} \\]

After twelve steps, the frequency doubles.

However, there is an important distinction: a twelve-note scale is not the same thing as a base-12 number system.

For example, seven equal-tempered semitones produce:

\\[ 2^{7/12}\approx1.498307 \\]

A just perfect fifth has the ratio:

\\[ \frac32=1.5 \\]

They are close, but not identical.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://physics.byu.edu\&sz=32)

physics.byu.edu+1



This gives us an excellent experiment:

Compare equal temperament against just intonation using frequency analysis, beat patterns and Lissajous figures.

We can investigate how small differences in frequency ratios change the resulting waveforms.

This is an established area of acoustics, but it offers an excellent testing ground for our numerical representations.

# **6. Experiment D: Modern digital signal processing**

Potential computational application

This is where I found a particularly interesting connection.

Modern signal processing already takes advantage of mathematical relationships involving the factors 2, 3 and 5.

The Fast Fourier Transform (FFT) is an algorithm that efficiently calculates the Discrete Fourier Transform (DFT).

The DFT is:

\\[ X[k]=\sum\_{n=0}^{N-1}x[n]e^{-i2\pi kn/N} \\]

The important detail is that FFT performance depends partly on how the number of samples, \\(N\\), can be factorised.

For example:

\\[ 60=2^2\times3\times5 \\]

And:

\\[ 12=2^2\times3 \\]

These are useful factorisations because mixed-radix FFT algorithms can exploit small prime factors.

SciPy's current FFT documentation explicitly describes how efficient small-prime-factor transforms influence performance and provides `next_fast_len()` to find useful transform sizes.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.scipy.org\&sz=32)

SciPy v1.18.0 Manual+1



**Why this is interesting**

# **12**

2 × 2 × 3

Dozenal factor structure

# **60**

2 × 2 × 3 × 5

Sexagesimal factor structure

These are precisely the types of small factors that many FFT implementations can handle efficiently.

This does NOT mean that writing numbers in base 60 makes a computer's FFT faster.

It means that transform lengths constructed from the same factors may be especially convenient for mixed-radix FFT implementations.

That is something we can measure.

### **D1. Benchmark different FFT sizes**

Compare:

| Family          | Example lengths         |
| --------------- | ----------------------- |
| Powers of two   | 1024, 2048, 4096, 8192  |
| 12-smooth       | 1728, 20736, 248832     |
| 60-smooth       | 3600, 216000            |
| Other 5-smooth  | Sizes selected by SciPy |
| Poorly factored | Nearby prime lengths    |

A 12-smooth length has only 2 and 3 as prime factors. A 60-smooth length can also contain 5.

We should benchmark several lengths around the same target size, rather than compare wildly different workloads.

### **D2. What to measure**

- FFT execution time.
- Memory consumption.
- Numerical precision.
- Forward/inverse transform accuracy.
- Frequency-bin spacing.
- Peak-frequency estimation error.
- Performance across different FFT lengths.
- Single-threaded versus multithreaded execution.

We must keep computational performance separate from the notation experiment.

For example, changing the length of an FFT can also change its frequency resolution. We cannot attribute every difference in output to the numerical base.

### **D3. Real signal processing**

After synthetic tests, use actual measurements.

[Playing flute without lips? Tones of music lost in time: An investigation of the indigenous Bastar flutes of India - Ashish Karn, Ritvik Anand, Aditya Kataria, Ramesh Kumar Donga, Naman Agarwal, Varun Pratap Singh, 2023](https://images.openai.com/static-rsc-4/2czK0zo4F3zrgQ3tb3E94KGiknVRLhPkh_iKy2MFN19mR66FYYHQWt5ovGArFW_bl6eyjfpq1EzrEq56wBIaXWgjoEP3AqLrpsR7sdtqF03zgucTkfZhb6ZIKkU6Fkn03m4zbdkyyCV_GmVNUaLeXPs8TM1kzkeF2KLiMo7ftSU?purpose=inline)

[Basics of Vibration Measurement and FFT Analysis | SHOWA SOKKI CORPORATION](https://images.openai.com/static-rsc-4/BsRAPGT-6Aqlf_mYMddiXw2wSvlnN60LC55z0dLranAN3tZlMBlYmtc-ozYCnlIQJkmxBSSNskOiIHLXQit9w1YXqoJheYmJB4IhR8pgTR2lKLQatarOy_GNnKTD0mCxRJNIVJPK6eGcDAfJBwQtq9BbTJfe1cAsAHLDH_ZvDXg?purpose=inline)

[Tektronix P5205A 1300V High Voltage Differential Probe - Partially Working | eBay](https://images.openai.com/static-rsc-4/FuLEhfdokMFzWPzzL7zupAHieOcsg0woqnubggUdM2a_1wdRF8l74XHzrycYXYkkhwPb6T1rWw4vR4wzsvU4ST65gBTHIEW9FByRrNgOFNOcrM-Ss1iBXDjsXcZVl1R8OPkJSuzoFtORYzR11I1T7cm_wyifSEmnyk5Q5pcvrQE?purpose=inline)

8

Test:

- Audio recordings.
- Mechanical vibration.
- Rotating motors and fans.
- Repetitive oscillations.
- Electrical-frequency signals.
- Combined signals containing multiple harmonics.

For each signal, preserve its original sampling rate, observation duration and physical units.

The sampling rate must be selected to preserve the frequency content being studied. The Nyquist-Shannon sampling theorem requires a sampling frequency greater than twice the highest frequency in a band-limited signal for ideal reconstruction.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.cs.cmu.edu\&sz=32)

CMU Intro to Computer Music+1



We should also control spectral leakage through consistent windowing. SciPy provides periodogram and other spectral-analysis tools for this purpose.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.scipy.org\&sz=32)

SciPy v1.18.0 Manual+1



# **7. Experiment E: Modular mathematics and cyclic patterns**

This brings back one of our earlier experiments.

We should investigate how 10, 12 and 60 behave in cyclic arithmetic.

For instance:

\\[ n\bmod 12 \\]

and:

\\[ n\bmod 60 \\]

These create different repeating sequences.

We can explore:

- Multiplication tables.
- Prime-number distributions.
- Divisibility patterns.
- Repeating sequences.
- Cyclic permutations.
- Modular inverses.
- Rotational symmetry.

[Create Your Own Math Clock](https://images.openai.com/static-rsc-4/SniM_a5wJDo1XJgVT9wliyfmH4mBdYqg3RzjTmUlw4bBI7MGDASj9NhdPCOJq6GMAZYtTrtT0AKdSyFlJ2-AiVw9AZYsfWuPtcm5qsQ64nmGcNf2ZRLvzZVTYZRxQ2iwvalpMy0IeM3y7cBAV8DXd0-hIl7bBoVkZzhbIwrof5Y?purpose=inline)

[mathcuriosity.com](https://www.mathcuriosity.com/post/math-of-clocks?utm_source=chatgpt.com)

One important distinction: base-12 notation and arithmetic modulo 12 are not the same mathematical operation.

We should explicitly test both, rather than accidentally treating them as equivalent.

For example, a multiplication table written in base 12 is a different experiment from a multiplication table reduced modulo 12.

This distinction matters because otherwise we might attribute a modular-arithmetic pattern to the numeral system itself.

# **8. Experiment F: Algebra and numerical pattern discovery**

This brings together our remaining earlier experiments.

The objective is to find out whether certain numerical structures become more intuitive under another representation.

### **F1. Polynomial relationships**

Compare expressions such as:

\\[ (x+1)^2,\quad (x+2)^2,\quad (x+3)^2 \\]

Investigate integer roots, factorisation, coefficient patterns and recurring sequences.

### **F2. Number sequences**

Generate:

- Fibonacci sequences.
- Triangular numbers.
- Square numbers.
- Cube numbers.
- Perfect numbers.
- Prime sequences.
- Geometric progressions.
- Harmonic sequences.

Render each sequence in all three numerical systems.

### **F3. Mathematical pattern discovery**

This is the most exploratory experiment.

Give the same datasets to a pattern-analysis system and ask it to identify relationships under each representation.

For each candidate discovery, require:

1. A mathematical statement.
2. An exact derivation or proof where possible.
3. An independent decimal representation.
4. A test against additional values.
5. A record of whether the relationship was already known.

We should not count a visually appealing pattern as a discovery until it has been independently verified.

# **9. Experiment G: Combining all the systems**

This is where I would look for the most interesting results.

Instead of studying fractions, geometry and signals independently, build experiments where all of them interact.

For example:

**A rotating object producing a vibration containing several harmonics.**

We can model it using:

- Angular rotation.
- Frequency.
- Time.
- Phase.
- Harmonic ratios.
- Geometric periodicity.
- Numerical fractions.

Then describe exactly the same behaviour using decimal, dozenal and sexagesimal representations.

[Frontiers | Nonlinear dynamic characteristics of wind power concentric planetary-face gear system with elastic lubrication and friction considering thermal effect under random wind load](https://images.openai.com/static-rsc-4/Td00FA0_ZZvCoGlHIXUIU-beUsjr8MIzuL-O9LbAUJfJyfn710dQn4gEF8SVDpZF5n2TRUFF-GDZu22ONy4opFMfL9N9ypqlAJRoGhfTNvH--glkMqLxTKGUUg4hasUiPoEl85L5QhaRlA5Y4PNaWbWEboUpb8dqkY2USy_bNGs?purpose=inline)

[frontiersin.org](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2024.1505956/full?utm_source=chatgpt.com)

### **Proposed combined experiment**

Start with a hypothetical rotating object:

- Fundamental frequency: 60 cycles per second.
- Second harmonic: 120 cycles per second.
- Third harmonic: 180 cycles per second.
- Fourth harmonic: 240 cycles per second.

Generate the combined signal and investigate:

1. How many cycles occur during different fractions of a second?
2. How do the individual harmonics align?
3. What happens when the phase is shifted by 1/12 or 1/60 of a rotation?
4. Which phase relationships produce repeating geometric patterns?
5. Can we represent the relationships more compactly in base 12 or base 60?
6. Do different FFT sample lengths make computational analysis more efficient?

Then repeat the experiment with irrational and non-terminating frequency ratios.

That last step is important because we don't want to investigate only examples that naturally favour base 12 or 60.

# **10. Experimental controls: preventing false discoveries**

I consider this one of the most important parts of the research.

We need to keep four different mathematical concepts separate.

| Concept             | What it represents                              |
| ------------------- | ----------------------------------------------- |
| Numerical base      | How numbers are written                         |
| Angular measurement | How rotations are measured                      |
| Modular arithmetic  | How repeating numerical cycles behave           |
| FFT factorisation   | How a computational transform can be decomposed |

These can interact, but they are not interchangeable.

For every experiment:

**Control 1 — Same mathematical quantity**

A value of 75 must remain 75 regardless of whether it is expressed in decimal, dozenal or sexagesimal.

**Control 2 — Exact arithmetic**

Use rational numbers and symbolic expressions whenever possible. Avoid introducing floating-point rounding into tests of mathematical identities.

**Control 3 — Independent verification**

Every potentially interesting pattern must be converted back to a canonical mathematical expression and independently verified.

**Control 4 — Equal experimental conditions**

For signal processing, preserve sampling rates, measurement durations and frequency content. For computational benchmarks, document transform sizes and software implementations.

**Control 5 — Negative results matter**

If base 60 performs worse than base 10 in an experiment, record that result.

We should also include randomly generated datasets and holdout tests. Otherwise, it is too easy to discover patterns simply because we selected examples that favour our preferred number system.

# **11. Software architecture**

I recommend building this as a self-contained experimental mathematics project.

**base12-base60-laboratory/**

&#x20;docs/

RESEARCH_PLAN.md

HYPOTHESES.md

EXPERIMENT_PROTOCOLS.md

RESULTS.md

&#x20;src/base60lab/

numerals.py — base conversion and arithmetic

fractions.py — reciprocals and division

angles.py — degrees, turns and radians

geometry.py — circles and polygons

trigonometry.py — trigonometric relationships

modular.py — cyclic arithmetic

sequences.py — number sequences and algebra

frequency.py — oscillations and harmonics

lissajous.py — phase and geometric plots

signal_processing.py — filters and spectral analysis

fft_benchmarks.py — FFT performance testing

metrics.py — comparison and evaluation

&#x20;experiments/

01_fraction_analysis.py

02_geometry_analysis.py

03_trigonometry_analysis.py

04_modular_patterns.py

05_algebra_sequences.py

06_harmonic_analysis.py

07_lissajous_analysis.py

08_fft_benchmarks.py

09_real_world_signals.py

10_combined_experiments.py

&#x20;tests/

&#x20;data/

&#x20;results/

&#x20;pyproject.toml

&#x20;README.md

### **Recommended technology**

Use Python 3.12 for the initial research engine.

| Library    | Purpose                                  |
| ---------- | ---------------------------------------- |
| SymPy      | Exact algebra and symbolic mathematics   |
| NumPy      | Numerical arrays and waveform generation |
| SciPy      | FFT and signal processing                |
| mpmath     | Arbitrary-precision calculations         |
| Matplotlib | Geometric and frequency visualisations   |
| Pandas     | Experimental results and comparisons     |
| pytest     | Automated validation                     |

I would keep the mathematical engine independent of the visualisation layer, so later we could create a browser dashboard or a faster Rust implementation without rewriting the research.

### **Required automated tests**

The test suite should verify:

- Base conversion round trips.
- Exact fraction conversions.
- Addition, subtraction, multiplication and division.
- Sexagesimal carry operations.
- Dozenal digit handling.
- Degree/radian/turn conversions.
- Trigonometric identities.
- Rational frequency relationships.
- FFT round-trip accuracy.
- Deterministic experimental results.

Every experiment should produce JSON results, CSV measurements and visualisations, including the configuration used to generate them.

# **12. Research roadmap and milestones**

I would approach this in seven stages.

## **Development roadmap**

1. **Milestone 1 — Numerical foundation**

   Start here

   Build the base-10, base-12 and base-60 conversion engine, exact fractions and automated tests.

   *Deliverable:* Validated multi-base mathematical engine.
2. **Milestone 2 — Arithmetic and geometry**

   Complete fraction analysis, reciprocals, divisibility, circles, polygons and trigonometric comparisons.

   *Deliverable:* Numerical comparison report and geometric visualisations.
3. **Milestone 3 — Frequency and harmonic research**

   Generate synthetic signals, investigate frequency ratios, phase alignment, beats and Lissajous figures.

   *Deliverable:* Harmonic research dataset and interactive visualisations.
4. **Milestone 4 — Digital signal processing**

   Benchmark FFT sizes, mixed-radix decomposition, spectral accuracy and computational performance.

   *Deliverable:* Reproducible benchmark report.
5. **Milestone 5 — Algebra and pattern discovery**

   Examine sequences, modular relationships and symbolic mathematics across all three representations.

   *Deliverable:* Verified mathematical pattern catalogue.
6. **Milestone 6 — Real-world signal validation**

   Apply the experiments to real audio, mechanical vibration and other measured oscillations.

   *Deliverable:* Real-world comparison report.
7. **Milestone 7 — Combined analysis**

   Bring all the findings together and identify where each mathematical representation has a demonstrable advantage.

   *Deliverable:* Final research paper, reproducible experiments and recommendations.

# **13. How we determine whether we discovered something useful**

I would use five measures.

| Measurement               | What it tells us                                                        |
| ------------------------- | ----------------------------------------------------------------------- |
| Representation efficiency | How compactly can we express a relationship?                            |
| Mathematical simplicity   | How easily can we manipulate it?                                        |
| Computational efficiency  | Does it reduce processing requirements?                                 |
| Visual interpretability   | Does it expose relationships more clearly?                              |
| Discovery effectiveness   | Does it help identify previously overlooked mathematical relationships? |

The last measure is particularly interesting.

We could conduct controlled problem-solving experiments where the same mathematical problems are presented in different representations, with presentation order randomised.

Record calculation accuracy, solution time and which patterns people identify.

This would help determine whether a base-12 or base-60 approach actually improves intuition, rather than simply looking more interesting.

# **14. What I expect we might discover**

These are predictions to test, not conclusions.

**Expected research outcomes**

**Fractions and reciprocals**

Strong theoretical advantage

Base 60 should perform particularly well for denominators composed of 2, 3 and 5.

**Geometry and trigonometry**

Worth investigating

Twelve-part and sixty-part angular representations may be useful for rotations, cyclic subdivisions and phase displays.

**Frequency and harmonics**

Worth investigating

Rational frequency relationships and repeating phase structures may become easier to organise and visualise.

**FFT performance**

Benchmark required

Twelve-smooth and sixty-smooth sizes may perform well with suitable mixed-radix implementations. Powers of two may still win on some implementations.

**Mathematical discovery**

Open question

A different representation could help us formulate useful conjectures, but any new relationship must be proven independently of its notation.

## **15. The most important research direction**

I would place particular emphasis on the relationship between:

\\[ \boxed{\text{Time}\quad\leftrightarrow\quad\text{Frequency}\quad\leftrightarrow\quad\text{Rotation}} \\]

These three quantities are mathematically connected.

A frequency describes cycles over time. A cycle describes a complete rotation of phase. Phase can be expressed as an angular measurement.

The connections are:

\\[ \omega=2\pi f \\]

\\[ \theta(t)=\omega t+\theta_0 \\]

\\[ T=\frac{1}{f} \\]

We can investigate these relationships in decimal, dozenal and sexagesimal representations without changing their underlying mathematical meaning.

[사인파(정현파)의 이해\]](https://images.openai.com/static-rsc-4/lofmQ0R41qNwhMC-YxujqDBCuIK7rugDdi0BQiXUVhhutPVXgPDfQSJP4g5nBpnrJCSHsAidHvQ1qQ1O6ginz1KTZba-XhVt9MpTfhq3JhjhZtvhEOPLfhrQ0CGwVmM9G5lvFbMCZXwXi2TFlmgFEIK7leZ_ZtpwtnqQrn-o7o8?purpose=inline)

[advancedtestingservices.tistory.com](https://advancedtestingservices.tistory.com/1972?utm_source=chatgpt.com)

**My recommendation is to make frequency, harmonics and phase the central theme of this project, with fractions and geometry providing its mathematical foundation.**

There is already a real mathematical connection worth examining: 12 contains the factors 2 and 3, while 60 adds the factor 5. Those factors occur naturally in the exact representation of many useful ratios and in mixed-radix computational methods.

The opportunity is not to prove that ancient mathematics contains secret laws of vibration. It is to find out whether a different numerical framework gives us a more useful way to explore relationships that modern mathematical notation sometimes makes less intuitive.

### **Research references**

These are good starting points for the project:

1. [The Open University — Babylonian Mathematics](https://www.open.edu/openlearn/mod/oucontent/view.php?id=1976\&printable=1\&utm_source=chatgpt.com) — historical mathematics and sexagesimal fractions.
2. [SciPy — FFT next_fast_len](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.next_fast_len.html?utm_source=chatgpt.com) — mixed-radix FFT sizing and performance.
3. [SciPy — Signal Processing](https://docs.scipy.org/doc/scipy/tutorial/signal.html?utm_source=chatgpt.com) — spectral analysis and signal processing.
4. [OpenStax — Trigonometric Functions](https://openstax.org/books/calculus-volume-1/pages/1-3-trigonometric-functions?utm_source=chatgpt.com) — radians, periodic functions and trigonometry.
5. [The Physics of Musical Scales](https://physics.byu.edu/docs/publication/2791?utm_source=chatgpt.com) — experimental investigation of frequency ratios and tuning.

**The direction I would take:** Build the research laboratory first, rather than immediately building a large visual application. Get the exact mathematics working, run the first three experiments, and let the results determine what deserves deeper investigation.

That gives us a foundation for eventually creating a genuinely useful alternative mathematical exploration environment, rather than just a base converter.
