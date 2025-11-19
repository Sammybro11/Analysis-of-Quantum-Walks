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

