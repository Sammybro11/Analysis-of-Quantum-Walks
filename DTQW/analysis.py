import numpy as np
import matplotlib.pyplot as plt
import Core
import Plotting
from pathlib import Path
from tqdm import tqdm


def defect_str_origin():
    N = 201
    center = 150
    t_max = 30
    times = np.linspace(0, t_max, t_max + 1, dtype = int)
    dir = Path("PlotAnalysis")
    dir.mkdir(parents = True, exist_ok = True)
    path = dir / "Defect_Origin.png"

    defect_range = np.linspace(-np.pi, np.pi, 30)
    prob_origin_balanced = []
    prob_origin_0 = []
    prob_origin_1 = []
    coin_state = np.array([np.array([1.0, 0.0 + 1.0j], dtype=complex) / np.sqrt(2), np.array([1.0, 0.0 + 0.0j], dtype=complex), np.array([0.0, 1.0 + 0.0j], dtype=complex)])

    for defect in tqdm(defect_range, desc = "Origin Strength Test"):
        for i in range(3):
            H_defected = Core.Hamiltonian(N)
            H_defected.addDefects([center], defect)

            Psi = Core.Wavefunction(gaussian = False, Num_sites= N, center = center, coin_init = coin_state[i])
            Evo = Core.Evolver(H_defected, Psi)

            _, prob = Evo.run(times)
            if i == 0:
                prob_origin_balanced.append(prob[-1][center])
            elif i == 1:
                prob_origin_0.append(prob[-1][center])
            elif i == 2:
                prob_origin_1.append(prob[-1][center])

    fig, ax = plt.subplots(figsize = (12, 10))
    ax.set_title("Probability at Origin vs Defect Strength", fontsize = 16)
    ax.plot(defect_range, prob_origin_balanced, label = r"Coin: $|0 \rangle + |1 \rangle$")
    ax.plot(defect_range, prob_origin_0, alpha = 0.5, linestyle = "dotted",label = r"Coin: $|0 \rangle$")
    ax.plot(defect_range, prob_origin_1, alpha = 0.5, linestyle = "dashdot", label = r"Coin: $|1 \rangle$")
    ax.set_xlabel("Defect Strength")
    ax.set_ylabel("Probability")
    ax.grid(True)
    ax.legend()
    plt.savefig(path, bbox_inches = "tight")

def transmission_prob():
    N = 201
    center = 150
    defect_distance = 15
    t_max = 30
    times = np.linspace(0, t_max, t_max + 1, dtype = int)
    dir = Path("PlotAnalysis")
    dir.mkdir(parents = True, exist_ok = True)
    path = dir / "Transmission.png"

    defect_range = np.linspace(-np.pi, np.pi, 30)
    prob_origin_balanced = []
    prob_origin_0 = []
    prob_origin_1 = []
    coin_state = np.array([np.array([1.0, 0.0 + 1.0j], dtype=complex) / np.sqrt(2), np.array([1.0, 0.0 + 0.0j], dtype=complex), np.array([0.0, 1.0 + 0.0j], dtype=complex)])

    for defect in tqdm(defect_range, desc = "Transmission Test"):
        for i in range(3):
            H_defected = Core.Hamiltonian(N)
            H_defected.addDefects([center + defect_distance], defect)

            Psi = Core.Wavefunction(gaussian = False, Num_sites= N, center = center, coin_init = coin_state[i])
            Evo = Core.Evolver(H_defected, Psi)

            _, prob = Evo.run(times)
            if i == 0:
                prob_origin_balanced.append(prob[-1][center + defect_distance:].sum())
            elif i == 1:
                prob_origin_0.append(prob[-1][center + defect_distance:].sum())
            elif i == 2:
                prob_origin_1.append(prob[-1][center + defect_distance:].sum())

    fig, ax = plt.subplots(figsize = (12, 10))
    ax.set_title("Transmission Probability vs Defect Strength", fontsize = 16)
    ax.plot(defect_range, prob_origin_balanced, label = r"Coin: $|0 \rangle + |1 \rangle$")
    ax.plot(defect_range, prob_origin_0, alpha = 0.5, linestyle = "dotted",label = r"Coin: $|0 \rangle$")
    ax.plot(defect_range, prob_origin_1, alpha = 0.5, linestyle = "dashdot", label = r"Coin: $|1 \rangle$")
    ax.set_xlabel("Defect Strength")
    ax.set_ylabel("Probability")
    ax.grid(True)
    ax.legend()
    plt.savefig(path, bbox_inches = "tight")

def trapping():
    N = 501
    defect_sites = [200, 300]
    defect_phase = np.pi/1.2

    dir = Path("PlotAnalysis")
    dir.mkdir(parents = True, exist_ok = True)
    path = dir / "Trapped.png"

    center = 250
    t_max = 550
    times = np.arange(0, t_max + 1, dtype=int)

    H_defected = Core.Hamiltonian(N)
    H_defected.addDefects(defect_sites, defect_phase)

    Psi = Core.Wavefunction(gaussian=False, Num_sites=N, center=center)

    Evo_defected = Core.Evolver(H_defected, Psi)

    vecs_defected, prob_defected = Evo_defected.run(times)

    trapped_prob = prob_defected[:, 200:300].sum(axis = 1)
    fig, ax = plt.subplots(figsize = (10, 10))
    ax.set_title("Trapped Probability vs Time", fontsize = 16)
    ax.plot(times, trapped_prob)
    ax.set_xlabel("Time")
    ax.set_ylabel("Probability")
    ax.grid(True)
    plt.savefig(path, bbox_inches = "tight")


if __name__ == "__main__":
    trapping()
