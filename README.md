# Analysis of Quantum Walks in Defected Lattices

> Please read `Report.pdf` for a deeper understanding of the project.

This repository contains the full code, simulations, and analysis for the project  
**“Analysis of Quantum Walks in Defected Lattices”**, carried out at the  
**Indian Institute of Technology, Hyderabad**.

The project investigates how single and multiple lattice defects affect transport in:

- Continuous-Time Quantum Walks (CTQW)  
- Discrete-Time Quantum Walks (DTQW)  
- Quantum circuit implementations of DTQWs on small cyclic lattices using Qiskit

We analyze localization, reflection, transmission, and trapping, comparing analytic predictions with numerical simulations and hardware-aware quantum-circuit models.

---

## Repository Structure

```
.
├── CTQW/
│   ├── Core.py                # Hamiltonian, wavefunction, evolver classes
│   ├── SimulationScripts/     # Localization, transmission, trapping scripts
│   └── Plots/                 # Resulting CTQW figures
│
├── DTQW/
│   ├── DTQW_Core.py           # Coin + shift based DTQW implementation
│   ├── DefectSimulations/     # Phase defect evolution and scattering
│   └── Plots/                 # DTQW plots
│
├── QuantumCircuits/
│   ├── RealWalk_2Bit.py       # 4-node cyclic walk
│   ├── RealWalk_3Bit.py       # 8-node cyclic walk
│   ├── results.json           # Ideal vs noisy distributions and metrics
│   └── Figures/               # Circuit-generated plots
│
├── Report/
│   └── Analysis_of_Quantum_Walks.pdf
│
└── README.md
```

---

## Project Overview

### 1. Continuous-Time Quantum Walk (CTQW)

CTQWs are implemented using a Laplacian-based Hamiltonian:

\[
H = 2I - A \quad\text{or}\quad H = D - A,
\]

with on-site potentials encoding defects:

\[
H = H_0 + \Gamma \sum_m |m\rangle\langle m|.
\]

Key phenomena investigated:

- Momentum-dependent reflection and transmission  
- Localization at strong defects  
- Formation of bound states  
- Trapping between two defects  
- Analytic scattering amplitude:
\[
T(k) = \frac{4\sin^2 k}{4\sin^2 k + \Gamma^2}
\]

---

### 2. Discrete-Time Quantum Walk (DTQW)

We use a Hadamard coin and conditional shift:

\[
U = S(C \otimes I),
\]

with phase defects introduced via:

\[
C_j = e^{i\phi_j} C_H.
\]

DTQW simulations reproduce the same qualitative behaviour seen in CTQW, including localization and scattering from defects.

---

### 3. Quantum Circuit Implementations (Qiskit)

We build explicit quantum circuits for cyclic DTQWs:

- 4-node walk (2 position qubits + coin)  
- 8-node walk (3 position qubits + coin, using an optimized increment/decrement construction)

Two modes of execution are supported:

- Ideal evolution (Qiskit Aer)
- Noise-aware evolution (IBM backend noise models)

We quantify the deviation between ideal and noisy distributions using the Hellinger distance.

---

## Key Results

- CTQW and DTQW show analogous scattering behaviour under localized defects.
- Single-defect transmission matches analytic theory across a wide momentum range.
- Two-defect systems show stable trapping and periodic escape peaks.
- Quantum circuits accurately reproduce the first few DTQW steps, but noise accumulation degrades long-time behaviour.
- Larger position registers (three qubits) are more sensitive to noise due to circuit depth.

---

## References

Key references include:

- Kempe, Quantum random walks — an introductory overview  
- Li et al., Position-defect-induced reflection, trapping, transmission, and resonance in quantum walks  
- Wójcik et al., Trapping in DTQWs  
- Farhi and Gutmann, CTQW on graphs  
- Douglas and Wang, Efficient quantum walk circuit constructions  
- Qiskit community tutorials on quantum walks  

Full references are available in the `Report/` directory.

---

