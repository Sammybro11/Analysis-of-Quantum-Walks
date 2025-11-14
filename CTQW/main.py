import numpy as np
import Core
import Plotting

def main():
    N = 400               # number of lattice sites
    center = 80          # center of initial Gaussian
    spread = 15           # width of Gaussian
    momentum = 0.8        # phase gradient / k

    # Defects
    def_positions = [150, 250]
    defect_strength = 4.0
    buffer = 2

    # Time grid
    t_max = 250
    nt = 300
    times = np.linspace(0, t_max, nt)


    # --- Create system ---
    H = Core.Hamiltonian(N)
    H.addDefects(def_positions, defect_strength)

    psi = Core.Wavefunction(N, center, spread, momentum)

    # Set up evolution manager
    evo = Core.Evolver(H, psi)


    # --- Run evolution ---
    vecs, probs, regions = evo.run_analyze(times, def_positions[0], def_positions[1], buffer)


    # --- Plot results ---
    print("Plotting region probabilities vs time...")
    Plotting.ProbEvol(times, regions)

    print("Plotting probability distribution at t_index = 100...")
    Plotting.ProbDist(probs, t_index=100)


if __name__ == "__main__":
    main()
