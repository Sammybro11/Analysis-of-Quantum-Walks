import numpy as np
import Core
import Plotting

def localization():
    N = 501               # number of lattice sites
    center = 250          # Center of Starting Wavefunction
    defect_strength = -2.0  # Defect Strength

    # Time grid
    t_max = 100
    times = np.linspace(0, t_max, t_max + 1, dtype = int)

    # Hamiltonians 
    H_free = Core.Hamiltonian(N)
    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects([center], defect_strength)

    Psi = Core.Wavefunction(gaussian= False, Num_sites = N, center = center) 

    Evo_free = Core.Evolver(H_free, Psi)
    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_free, prob_free = Evo_free.run(times)
    vecs_defected, prob_defected = Evo_defected.run(times)
    probs = np.stack([prob_free, prob_defected])

    Plotting.ProbDistAnimate(probs, times, "Localization_Combined", 0.22)

def reflection():
    N = 1001
    defect_site = 600
    defect_strength = 1.0
    center = 400
    t_max = 300

    times = np.linspace(0, t_max, t_max + 1, dtype = int)

    H_free = Core.Hamiltonian(N)
    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects([defect_site], defect_strength)

    Psi = Core.Wavefunction(gaussian= False, 
                            Num_sites = N, 
                            center = center, )

    Evo_free = Core.Evolver(H_free, Psi)
    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_free, prob_free = Evo_free.run(times)
    vecs_defected, prob_defected = Evo_defected.run(times)
    probs = np.stack([prob_free, prob_defected])

    Plotting.ProbDistAnimate(probs, times, "Reflection_Delta", 0.1)

def reflection_gaussian():
    N = 1001
    defect_site = 600
    defect_strength = 1.0
    center = 400
    spread = 25
    momentum = 1.5
    t_max = 300

    times = np.linspace(0, t_max, t_max + 1, dtype = int)

    H_free = Core.Hamiltonian(N)
    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects([defect_site], defect_strength)

    Psi = Core.Wavefunction(gaussian= True, 
                            Num_sites = N, 
                            center = center, 
                            spread = spread, 
                            momentum = momentum ) 

    Evo_free = Core.Evolver(H_free, Psi)
    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_free, prob_free = Evo_free.run(times)
    vecs_defected, prob_defected = Evo_defected.run(times)
    probs = np.stack([prob_free, prob_defected])

    Plotting.ProbDistAnimate(probs, times, "Reflection_Gaussian", 0.1)

def trapping():
    N = 1001
    defect_sites = [400, 600]
    defect_strength = 8.0

    center = 500
    t_max = 250
    times = np.linspace(0, t_max, t_max + 1, dtype = int)

    H_free = Core.Hamiltonian(N)
    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects(defect_sites, defect_strength)

    Psi = Core.Wavefunction(gaussian= False, 
                            Num_sites = N, 
                            center = center,) 

    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_defected, prob_defected = Evo_defected.run(times)
    probs = np.stack([prob_defected])

    Plotting.ProbDistAnimate(probs, times, "Trapping_Delta", 0.1)

def trapping_gaussian():
    N = 1001
    defect_sites = [400, 600]
    defect_strength = 8.0

    center = 500
    spread = 15
    momentum = 1.0
    t_max = 250
    times = np.linspace(0, t_max, t_max + 1, dtype = int)

    H_free = Core.Hamiltonian(N)
    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects(defect_sites, defect_strength)

    Psi = Core.Wavefunction(gaussian= True, 
                            Num_sites = N, 
                            center = center, 
                            spread = spread, 
                            momentum = momentum ) 

    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_defected, prob_defected = Evo_defected.run(times)
    probs = np.stack([prob_defected])

    Plotting.ProbDistAnimate(probs, times, "Trapping_Gaussian", 0.1)

if __name__ == "__main__":
    localization()
    reflection()
    trapping()
    reflection_gaussian()
    trapping_gaussian()
