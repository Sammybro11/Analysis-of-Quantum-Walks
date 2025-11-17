import numpy as np
import Core
import Plotting

def localization():
    N = 501               # number of lattice sites
    center = 250          # Center of Starting Wavefunction
    defect_phase = np.pi  # defect phase (radians)

    # Time grid
    t_max = 100
    times = np.arange(0, t_max + 1, dtype=int)

    # Hamiltonians 
    H_free = Core.Hamiltonian(N)
    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects([center], defect_phase)

    Psi = Core.Wavefunction(gaussian=False, Num_sites=N, center=center)

    Evo_free = Core.Evolver(H_free, Psi)
    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_free, prob_free = Evo_free.run(times)
    vecs_defected, prob_defected = Evo_defected.run(times)
    probs = np.stack([prob_free, prob_defected])

    Plotting.ProbDistAnimate(probs, times, "Localization_Combined_DTQW", 0.22)

def reflection():
    N = 1001
    defect_site = 600
    defect_phase = np.pi/2
    center = 500
    t_max = 500

    times = np.arange(0, t_max + 1, dtype=int)

    H_free = Core.Hamiltonian(N)
    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects([defect_site], defect_phase)

    Psi = Core.Wavefunction(gaussian=False, Num_sites=N, center=center)

    Evo_free = Core.Evolver(H_free, Psi)
    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_free, prob_free = Evo_free.run(times)
    vecs_defected, prob_defected = Evo_defected.run(times)
    probs = np.stack([prob_free, prob_defected])

    Plotting.ProbDistAnimate(probs, times, "Reflection_Combined_DTQW", 0.1)

def trapping():
    N = 1001
    defect_sites = [400, 600]
    defect_phase = np.pi

    center = 500
    t_max = 550
    times = np.arange(0, t_max + 1, dtype=int)

    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects(defect_sites, defect_phase)

    Psi = Core.Wavefunction(gaussian=False, Num_sites=N, center=center)

    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_defected, prob_defected = Evo_defected.run(times)
    probs = np.stack([prob_defected])

    Plotting.ProbDistAnimate(probs, times, "Trapping_Combined_DTQW", 0.1)

if __name__ == "__main__":
    localization()
    reflection()
    trapping()
