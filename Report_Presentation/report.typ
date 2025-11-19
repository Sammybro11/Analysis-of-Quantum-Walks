// #import "@preview/basic-report:0.3.1": *
#import "@preview/red-agora:0.1.2": project
#import "@preview/quill:0.7.2": *

#show: project.with(
  title: "Analysis of Quantum Walks in Defected Lattices",
  subtitle: "Mathematical Physics Project",
  authors: (
    "Samyak Rai",
    "EP24BTECH11026",
    "Engineering Physics"
  ),
  mentors: (
    "Prof. Sangkha Borah",
  ),
  branch: "IIT Hyderabad",
  academic-year: "2025-2026",
  footer-text: "IITH"
)

= Introduction

Quantum walks are the quantum analog to the classical random walk, extended to take into account superposition, interference, and quantum correlations.
It provides a comprehensive framework to study quantum dynamics in discrete and structured space. 
Compared to the classical random walk, quantum walks exhibit markedly different behavior; for instance, a quantum walk can propagate quadratically faster than its classical counterpart, 
is a time-reversible process rather than a memoryless Markov process, and results in a probability distribution drastically different from the classically expected Gaussian @Intro_Kempe

As with classical random walks, there are two related but fundamentally different formulations of quantum walks—the discrete-time quantum walk (DTQW) and the continuous-time quantum walk (CTQW). 
Due to their unintuitive dynamical behavior, quantum walks have been extensively explored over the past decade, which may provide methods of modeling complex biological systems  or hold the key to radical new quantum algorithms. @Intro_Kempe

In CTQW, disorder can be represented by position- or time-dependent potential defects in the diagonal elements of the transition matrix. 
In DTQW, disorder is introduced through the coin operator; the position-dependent coin provides static disorder, while the time-dependent coin gives rise to dynamic disorder.
In this report, we study the scattering properties of quantum walks, including localization, reflection, and trapping for both CTQW and DTQW with a wide range of defect settings. 
In particular, we investigate the roles played by the potential defects in CTQW and the phase defects in DTQW with respect to the control of quantum walk behaviors.@Intro_Yin 

We also explore the real life implementation of DTQW on cyclic lattices and their accuracy and fidelity, to understand the current challenges faced by the industry in implementation of such models. We use Qiskit's Circuit designing methods and their Runtime Service Noise simulation models to give accurate representation of hardware.

= Mathematical Model <Sec2>

The general idea for a Random walk is, for a walker to start at some point and to move left and right on the lattice with equal probability, 
to achieve this for Quantum Walkers which might exhibit properties such as superposition we use 2 different models, they construction of both models is different, however the exhibit the same properties in their walkers.

== Discrete Time Quantum Walk

Let $cal(H)_p$ be the Hilbert Space spanned by the position of the walker. 
For a line of with grid-length 1 this space is spanned by basis states ${|i angle.r : i = 0, ... , N+1 }$. 
The position space is augmented by a "Coin Space" $cal(H)_c$ spanned by two basis states ${| arrow.t angle.r, | arrow.b angle.r }$, which take the role of the spin-$1/2$. 
States of the whole system are in the $cal(H) = cal(H)_p times.circle cal(H)_c$. A single time step of evolution is $U = S C$, where $C$ is the coin operator and $S$ is the shift operator. @Kempe_2003

The Hadamard Coin operator is defined as, 
$ C_H = 1/sqrt(2) mat(1 , 1 ; 1 , -1) $
and the Shift operator is defined as, 
$ S = |arrow.t angle.r angle.l arrow.t| times.circle sum_i |i + 1 angle.r angle.l i| + |arrow.b angle.r angle.l arrow.b| times.circle sum_i |i -1 angle.r angle.l i| $

Let $a_j(t)$ and $b_j(t)$ denote the amplitudes of $|j , arrow.t angle.r$ 
and $|j, arrow.b angle.r$. After applying the Hadamard coin at site $j$,
$ mat( a_j'(t) ; b_j'(t) ) = 1/sqrt(2) mat(1 , 1 ; 1 , -1) mat( a_j(t); b_j(t) ) $
The conditional shift then moves the amplitudes:
$ a_j(t+1) = a'_(j-1)(t), quad b_j(t+1) = b'_(j+1)(t). $
These two relations specify the deterministic, unitary time evolution.

The major point of difference between the classical and quantum implementation of the discrete time walk is the use of a quantum, rather than classical, 
coin operator—with the result that the walker now has the possibility of being in a superposition of possible coin states $|c angle.r$ at every step. 
It should be noted that the resulting coherence is a source of most of the counterintuitive behavior of the DTQW; 
if the coin operator is applied randomly, or if we were to measure the coin state after each time step, the superposition is destroyed and we recover the classical random walk. @Li_Main

=== Phase Defect

Now we introduce a phase defect into our Unitary Time stepping operator, to do this we modify the coin, instead of having a coin which is symmetric for all lattice points, we add phase shift to the coin at the lattice points we want to induce a defect.
$ C_("defect") = cases( e^(i phi) C_H &"if" j = "defect", C_H &"if" j != "defected" ) $
where $phi$ is our phase defect.

== Continuous Time Quantum Walk

The idea of a Continuous time Quantum Walk was first proposed by Farhi and Gutmann @Farhi, to establish a general framework for study of coherent transport systems. 
The continuous-time quantum walk can be regarded as a quantization of the corresponding classical continuous-time random walk, with the system now evolving as per the Schrödinger equation rather than the Markovian master equation. As a result, classical probabilities are replaced by quantum probability amplitudes. @Li_Main

=== Laplacian Matrix <Lap_Sec>

To understand continuous-time random walk on a discrete graph $G(V, E)$, composed of $n$ unordered vertices $j in V$, and edges $e_i = (j, k) in E$ we need to use a _Laplacian Matrix_ $L_(n times n)$ defined as follows, 

$ L_(i j) := cases( "deg"(v_i) &"if " i =j , 1 &"if " |i -j| = 1, 0 &"otherwise" ) $
or equivalently, $ L = D - A $ where $D$ is the degree matrix for the graph and $A$ is the adjacency matrix.

Now we can define our Hamiltonian for CTQW in two ways: $ H = gamma A quad H = L = D - A $
Adding the Degree matrix acts as Potential Measure for each node, which in someways represents the Potential Barriers in Motion.

Classically, the state of the random walker is fully described by the probability distribution vector $P(t)$, with its time evolution governed by the master equation,
$ (dif P(t))/ (dif t) = H P(t). $
which has a formal solution as $P(t) = e^(-H t)P(0)$. A standard classical choice is $H = -L$, producing diffusive spreading.

For the continuous-time quantum walk (CTQW), the Hamiltonian
governs unitary Schrodinger evolution,
$ i dif / (dif t)|psi(t)angle.r = H |psi(t)angle.r, quad |psi(t)angle.r = e^(-i H t)|psi(0) angle.r $
Two related Hamiltonians are commonly used:
$ H = gamma A quad "or" quad H = L = D - A. $
The adjacency-based Hamiltonian generates pure hopping dynamics, while
the Laplacian adds a uniform on-site term $D$ that acts as a 
*position-dependent potential*.  

On regular graphs, adding $D$ amounts only to a global phase:
$ e^(-i L t) = e^(-i(2I - A)t) = e^(-2 i t)\,e^(i A t), $
so both choices produce identical probability distributions.
The Laplacian form, however, has two advantages:
it resembles the discrete kinetic-energy operator
and it allows natural incorporation of *defects* or 
site-dependent potentials by modifying diagonal entries.

This makes the Laplacian particularly useful when modelling
lattices with localized perturbations, barriers, or impurities,
as required for studying scattering, localization, and trapping in CTQWs.
Thus, the wavefunction for a CTQW can be described as such, 
$ e^(-i L t) = e^(-i ( 2I - H_A )t) = e^(-2I t) e^(i H_A t) $
Since the global phase can be ignored we can say, the evolution of the wavefunction in equivalent in both cases. 
Using Laplacian allows us to model a potential for each node, which allows for easier conversion to lattices with defects.

=== Lattice Defects <Def_Sec>

To incorporate reflecting barriers or defects into our CTQW, we alter
the Hamiltonian by adding a real diagonal operator
$ Gamma = sum_(m) Gamma_m |m angle.r angle.l m|, $
where each $Gamma_m > 0$ represents the strength of a defect located
at site $m$.  The full Hamiltonian becomes
$ H = H_0 + Gamma. $
Such diagonal perturbations break the translational symmetry of the lattice and act as localized potentials.
These potentials modify the propagation of plane waves, allowing reflection, transmission, and the
formation of bound states localized around the defect sites. @Li_Main

The probability of finding the walker at node $j$ at time $t$ is given
by
$ P_j (t)= |angle.l j|e^(-i H t)|psi(0)angle.r|^2, $
and defects generate characteristic signatures in $P_j (t)$ such as
localized peaks, trapped probability between multiple barriers, or
suppressed transmission.  These features will be central to our study
of position defects in CTQWs.


= Effects of Lattice Defects

== Localization at Origin

We implement a quantum walk starting at origin with a defect at the origin itself $|j = 0 angle.r$, we observe in figure both CTQW and DTQW depict similar evolution with a large probability being bounded at the origin and rest of the walk progressing at ballistic speed $sigma ~ t$, with smaller peaks as compared to the undefected quantum walk.
#figure(
    caption: text[Probability distribution for (a) CTQW with $Gamma = 2$ at $t = 75$, (b) DTQW with $phi = pi$ at $t = 100$ \ Ideal quantum walk is shown in blue, and the defected quantum walk is shown in orange],
    grid(columns: 2,
    [#image("CTQW_Localization.png", alt: "Continuous Time Quantum Walk")],
    [#image("DTQW_Localization.png")],
    [#text(size: 0.7em)[(a) Continuous Time Quantum Walk]],
    [#text(size: 0.7em)[(b) Discrete Time Quantum Walk]],
    [$quad$], [$quad$]
    )
)

The similarity of the DTQW and CTQW probability distributions in Fig. 1 suggests the possibility of manipulating the DTQW coin degrees of freedom, in an attempt to reproduce the CTQW physical effects attributed to the point defects.

#figure(
    caption: text[Probability at origin at time $t = 30$ as function of (a) defect potential $Gamma$, and (b) phase defect at origin $phi$ with different initial coin states $|0 angle.r + |1 angle.r$, $|0 angle.r$ and $|1 angle.r$ ( last to are superimposed)],
    grid(columns: 2,
    [#image("CTQW_Defect_Origin.png")],
    [#image("DTQW_Defect_Origin.png")],
    [#text(size: 0.7em)[(a) Continuous Time Quantum Walk]],
    [#text(size: 0.7em)[(b) Discrete Time Quantum Walk]],
    [$quad$], [$quad$]
    )
)

We observe that coin states $|0 angle.r$ and $|1 angle.r$ are closer to the distribution of the Continuous Time Quantum,
further modification of the initial coin state or changing the Hadamard coin to other possible coins can allow us to further implement a closer simulation discrete time of a CTQW. 

Konno @Konno and Wojick et al. @Wojick have shown different forms of localization results by implementating different coins,
Fourier coins by Luarita et al. @Laurita are also known to show increased localization. 
This is an open problem as we explore different forms of coins and their localization properties.
#pagebreak()
== Reflection and Transmission Probability

Next, we discuss the case where the single point defect is located away from where the quantum walk starts. 
For our Continuous time Quantum Walk we consider a gaussian wave packet starting from $N = 400$ moving towards a lattice defect site at $N= 600$, we use this for easier visualization. A similar CTQW can be obtained by using a delta at center of lattice having it evolve in both directions.
In the Discrete time Quantum Walk we start an initial balanced state for propagation on both sides and then have it propagate with a single defect at $N = 600$ again.

#figure(
    caption: text[Probability distribution for (a) CTQW with $Gamma = 1$ at $t = 75$, (b) DTQW with $phi = pi/2$ at $t = 100$ \ Ideal quantum walk is shown in blue, and the defected quantum walk is shown in orange],
    grid(columns: 2,
    [#image("CTQW_Reflection.png", alt: "Continuous Time Quantum Walk")],
    [#image("DTQW_Reflection.png")],
    [#text(size: 0.7em)[(a) Continuous Time Quantum Walk]],
    [#text(size: 0.7em)[(b) Discrete Time Quantum Walk]],
    [$quad$], [$quad$]
    )
)

Some important features to note: 
- It evolves symmetrically in both the left and right direction, which is identical to a “free”quantum walk prior to its interaction with the barrier; 
- upon interacting with the barrier, it is largely reflected with a small probability of transmission; 
- The transmitted component continues to evolve ballistically as per the free quantum walk; 
- The larger the defect potential, the weaker the transmitted amplitude, as shown in Fig. 4(a); and (5) the reflected component interferes with the original propagating component, resulting in a complex interference pattern and asymmetric distribution compared to the free quantum walker. @Li_Main

=== Transmission Probability

#figure(
    caption: text[Probability distribution for (a) CTQW with $Gamma = 1$ at $t = 75$, (b) DTQW with $phi = pi/2$ at $t = 100$],
    grid(columns: 2,
    [#image("CTQW_Transmission.png", alt: "Continuous Time Quantum Walk")],
    [#image("DTQW_Transmission.png")],
    [#text(size: 0.7em)[(a) Continuous Time Quantum Walk]],
    [#text(size: 0.7em)[(b) Discrete Time Quantum Walk]],
    [$quad$], [$quad$]
    )
)

This time we see $|0 angle.r$ to have a higher transmission probability than both the other cases, this is due to the relation of the transmission probability with not just the defect potential but also the momentum of the wavepacket, we have observed that the transmission probability is dependent as follows: 
$ T(k) = (4 sin^2(k))/(4 sin^2(k) + mu^2) $
where $k$ is momentum of wavepacket and $mu$ is defect potential.

As discussed earlier in @Def_Sec, introducing a single defect corresponds to modifying the free
Hamiltonian $H_0$ by a local potential,
$ H = H_0 + Gamma |j angle.r angle.l j|.$
In the defect-free region, plane-wave solutions of the form
$psi_j = e^(i k j)$ satisfy the dispersion relation
$
E(k) = 2 (1 - cos(k)).
$

To analyse scattering from the defect ( assuming site to be at origin for ease ), we use the standard stationary
ansatz:
$ psi_j = cases(
e^(i k j) + r e^(-i k j) & j<0, 
t e^(i k j) & j>0 ) $
where the incoming wave $e^(i k j)$ is partially reflected and partially
transmitted with complex amplitudes $r(k)$ and $t(k)$.
Substituting this ansatz into the discrete Schrödinger equation and enforcing
the matching conditions at $j=0$ yields
$
r(k) = (Gamma)/(2 i sin k - Gamma),
quad
t(k) = (2 i sin k)/(2 i sin k - Gamma). $

The transmission probability is therefore
$
T(k) = |t(k)|^2
     = (4 sin^2 k)/(4 sin^2 k + Gamma^2 ),
$
which displays the characteristic Lorentzian-type suppression familiar from
one-dimensional scattering theory. @Wojick

#figure(
    caption: text[Transmission Probability of a Quantum Walk Gaussian with a defect Potential $Gamma = 2$, at $k = pi/2$ we observe the saturation as described by the formula ],
    image("Transmission_momentum.png", width: 60%)
)

Thus a single on-site defect acts as a momentum-dependent barrier.  The form
of $T(k)$ mirrors the textbook result for scattering from a delta-function
potential in the continuum, with $Gamma$ playing the role of the defect
strength and $sin k$ replacing the free-particle wavevector.


== Trapping

Finally we consider the scenario where the quantum walk starts at the center, however we have 2 defects in the lattice on both sides of the walker, this leads to the walker being reflected from both sides and being trapped inside the region. Since the spread of the walker doesn't change after being defected, the time taken by the walker to go from one lattice defect doesn't change. We can use this property to create timer like objects in lattices.


#figure(
    caption: text[Probability distribution for (a) CTQW with $Gamma = 1$ at $t = 150$, (b) DTQW  $phi = pi$ at $t = 350$ \ Ideal quantum walk is represented by blue in CTQW, whereas in DTQW no ideal walk is show],
    grid(columns: 2,
    [#image("CTQW_Trapping.png", alt: "Continuous Time Quantum Walk")],
    [#image("DTQW_Trapping.png")],
    [#text(size: 0.7em)[(a) Continuous Time Quantum Walk]],
    [#text(size: 0.7em)[(b) Discrete Time Quantum Walk]],
    [$quad$], [$quad$]
    )
)

Both Figs. 5(a) and 5(b) demonstrate similar behavior with the probability distribution mostly confined between the two barriers. Smaller group peaks are observed outside the barriers, which are symmetric about the origin, and their amplitudes depend on the strength of the defect potential $Gamma$ for CTQW and the phase defect $phi$ for DTQW. It is interesting to note that the gap between the consecutively transmitted group peaks is simply the distance between the two reflecting barriers, which suggests that the walker is reflected each time it interacts with a defect barrier and consequently bounces back and forth in between. @Li_Main

#figure(
    caption: text[Discrete time Quantum Walk with $phi = pi/2$. Trapped Probability inside the lattice defect sites as time progresses],
    image("Trapped.png", width: 40%)
)


= Quantum Circuits for Cyclic Lattices


To study how a discrete-time quantum walk behaves on present-day quantum hardware, we implemented explicit quantum circuits that simulate a walker on a cyclic lattice. 
The implementation mirrors the mathematical structure of the DTQW:
a single coin qubit controls left/right motion, and a register of position qubits encodes the lattice sites. 

== Simulation Specifications

The simulation was conducted locally by using qiskit's Aer Simulation package @qiskit2024, due the package version constraints we used python 3.12

*Qiskit Version* 
```bash
python                3.12.3
qiskit                2.2.3
qiskit-aer            0.17.2
qiskit-ibm-runtime    0.43.1
```

== Accuracy Metrics

To measure the accuracy of the noise simulation we use a metric known as _Hellinger Distance_, it's range is $[0, 1]$ with maximum accuracy when Heliinger Distance is 0. It's defined as follows,

For two probability distributions $P = (p_1, p_2, ..., p_k )$ and $Q = (q_1, q_2, ..., q_k)$ the hellinger distance between them is defined as, 
$ cal(H)(P, Q) = sqrt(sum_i (sqrt(P(i)) - sqrt(Q(i)))^2) $
It is equivalent to taking a euclidean norm between two vectors.

Furthermore, we define another metric, known as the _Hellinger Fidelity_ which forms the probability counterpart for fidelity between two vectors, 
$ cal(F)(P, Q) = (1 - cal(H)^2)^2 $

== Four Node Cyclic Quantum Walk

#align(center)[
    #image("4node.png", width: 40%)
]

To implement a quantum walk on a lattice with 4 nodes, we encode the position into 2 qubits and have a third register for the "Coin" the Quantum Circuit which is used is given below. @Wadhia


#align(center)[
    #quantum-circuit(
    lstick($|00 angle.r$, n: 2), 2, targ(), 2, 2, targ(), 2, setwire(1, stroke: (dash: "dashed")), 2,   meter(n: 1), [\ ],
    2, targ(), 2, targ(),1, targ(), 2, targ(), setwire( 1, stroke: (dash: "dashed")), 2, meter(n: 1), [\ ],
    lstick($|0 angle.r$), $H$, ctrl(-1), ctrl(-2), $X$, ctrl(-1), $H$, ctrl(-1), ctrl(-2), $X$, ctrl(-1),
    gategroup(3, 4, x: 2, y: 0, label: (pos: top, content: text[step])),
    gategroup(3, 4, x: 7, y: 0, label: (pos: top, content: text[step]))
)
]

It represents two steps of the walk, multiple iterations of the same operations with a Hadamard coin reset can be done to obtain a quantum walk for the required step count.

#figure(
    caption: "Discrete time Quantum Walk for a 2 Qubit Lattice. Panels 1 - 5 show steps 0 to 4 of the walk respectively. The bars represent the probability of finding the walker at a specific node. Blue bars represent Ideal results and Red bars represent results from the Qiskit Noise Simulator",
    image("plots_4node.png")
)

== Eight Node Cyclic Quantum Walk

#align(center)[
    #image("8_white.jpg", width: 50%)
]

Similarly to implement a quantum walk on a lattice with 8 nodes, we encode the position in 3 qubits and have a fourth quantum register for the "Coin",
however the shift operation for this would require a "C3X" gate, so instead we use a more efficient and optimized implementation by Douglas and Wang(2009) @Douglas_QC, 
the code implementation used is from the qiskit community tutorial on Advanced Quantum Walks @Qiskit

The Qiskit Implementation of the circuit is as follows, 

#align(center)[
    #image("circuit.png")
]

This represents a single step in the 8 node walk, the gates used in this consist of virtual gates and controlled phase shifts. The output produced on the Noise Aer Simulator by Qiskit is given below.


#figure(
    caption: "Discrete time Quantum Walk for a 3 Qubit Lattice. 
 Panels 1 - 7 show steps 1 to 7 of the walk respectively. The bars represent the probability of finding the walker at a specific node. Blue bars represent Ideal results and Red bars represent results from the Qiskit Noise Simulator",
    image("plots_8node.png", width: 90%)
)
#pagebreak()
As the size of the position register increases, the quantum walk circuit grows substantially in depth and gate count.
A walk on a cycle of $2^n$ nodes requires $n$ qubits for the position and an additional coin qubit.
Each step of the walk applies:
 - a coin operation, and
 - a conditional shift implemented using multi-controlled increment/decrement operations on all $n$ position qubits.

The cost of these multi-controlled updates grows roughly as $cal(O)(n dot.c "depth of "C n X)$, which already becomes considerable for $n >= 3$
Even after decomposition into native two-qubit gates, a single walk step for an 8-node lattice involves dozens of CNOTs and controlled-phase operations. Because the walk must be iterated step-by-step, the circuit depth increases linearly with the number of time steps.

For larger lattices, such as $N=100$ sites—which would require around seven position qubits—the problem becomes prohibitive.
A single controlled shift on seven qubits requires deep decompositions into two-qubit gates, and performing even 20–30 time steps results in thousands of elementary operations.
Contemporary NISQ devices cannot maintain coherent evolution over such depths, and even noise simulators struggle to capture the required error propagation realistically.
Thus, while small (4- or 8-node) cyclic quantum walks can be reproduced faithfully, the simulation of large $100+$-site walks lies beyond the reach of present architectures due to the exponential growth in circuit complexity and error accumulation.

= Conclusions

In this report, we examined how position-dependent defects shape the behaviour
of both continuous-time and discrete-time quantum walks on one-dimensional
lattices.  By developing parallel mathematical models for CTQW and DTQW, we
showed that on-site potentials in the continuous-time setting and local
coin-phase modifications in the discrete-time setting generate strikingly
similar physical phenomena: static localization at defect sites, momentum-
dependent reflection and transmission, the formation of bound states, and
the trapping of walkers between multiple barriers.  
These effects are governed by analytically tractable scattering amplitudes,
most notably the single-defect transmission probability
$T(k)=(4 sin^2(k))/(4 sin^2(k)+ Gamma^2),$
which provides a direct link between lattice defects and transport
suppression in quantum systems.

We also implemented discrete-time walks on four and eight node cyclic
lattices using quantum circuits built in Qiskit.  
The noise modeled simulations confirmed that short-time quantum walk
dynamics can be reproduced reliably on current noisy devices, while longer
evolutions accumulate gate and measurement errors that distort interference
patterns and probability distributions.  
Taken together, these results highlight both the conceptual clarity and the
experimental challenges of using quantum walks as probes of defects and
transport on discrete structures.  
As quantum hardware matures and circuit depth limitations ease, such
defect-engineered quantum walks may provide a practical route toward
quantum simulation of disordered media, quantum transport, and
interference-based sensing.

#pagebreak()

#bibliography("references.bib", style: "american-physics-society")
