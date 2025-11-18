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

    defect_range = np.linspace(-15, 15, 60)
    prob_origin = []

    for defect in tqdm(defect_range, desc = "Origin Strength Test"):
        H_defected = Core.Hamiltonian(N)
        H_defected.addDefects([center], [defect])

        Psi = Core.Wavefunction(gaussian = False, Num_sites= N, center = center)
        Evo = Core.Evolver(H_defected, Psi)

        _, prob = Evo.run(times)
        prob_origin.append(prob[-1][center])

    fig, ax = plt.subplots(figsize = (12, 10))
    ax.set_title("Probability at Origin vs Defect Strength", fontsize = 16)
    ax.plot(defect_range, prob_origin, label = "Probability at Origin")
    ax.set_xlabel("Defect Strength")
    ax.set_ylabel("Probability")
    ax.grid(True)
    plt.savefig(path, bbox_inches = "tight")

def transmission_prob():
    N = 201
    center = 150
    t_max = 30
    momentum = 0.8
    spread = 10
    defect_distance = 15
    times = np.linspace(0, t_max, t_max + 1, dtype = int)

    dir = Path("PlotAnalysis")
    path = dir / "Transmission.png"

    defect_range = np.linspace(-15, 15, 60)
    transmission_prob = []
    for defect in tqdm(defect_range, desc = "Transmission Test"):
        H_defected = Core.Hamiltonian(N)
        H_defected.addDefects([center + defect_distance], [defect])

        Psi = Core.Wavefunction(gaussian = True, Num_sites= N, center = center, spread= spread, momentum= momentum)
        Evo = Core.Evolver(H_defected, Psi)

        _, prob = Evo.run(times)
        transmission_prob.append(prob[-1][center + defect_distance:].sum())

    fig, ax = plt.subplots(figsize = (12, 10))
    ax.set_title("Transmission Probability vs Defect Strength", fontsize = 16)
    ax.plot(defect_range, transmission_prob, label = "Probability at Origin")
    ax.set_xlabel("Defect Strength")
    ax.set_ylabel("Probability")
    ax.grid(True)
    plt.savefig(path, bbox_inches = "tight")


def transmission_prob_momentum():
    N = 201
    center = 150
    t_max = 30
    defect_strength = 2.0
    spread = 10
    defect_distance = 15
    times = np.linspace(0, t_max, t_max + 1, dtype = int)

    dir = Path("PlotAnalysis")
    path = dir / "Transmission_momentum.png"

    momentum_range = np.linspace(0, np.pi/2, 20)
    transmission_prob = []
    for momentum in tqdm(momentum_range, desc = "Transmission Momentum Test"):
        H_defected = Core.Hamiltonian(N)
        H_defected.addDefects([center + defect_distance], [defect_strength])

        Psi = Core.Wavefunction(gaussian = True, Num_sites= N, center = center, spread= spread, momentum= momentum)
        Evo = Core.Evolver(H_defected, Psi)

        _, prob = Evo.run(times)
        transmission_prob.append(prob[-1][center + defect_distance:].sum())

    fig, ax = plt.subplots(figsize = (12, 10))
    ax.set_title("Transmission Probability vs Momentum of Wave Packet", fontsize = 16)
    ax.plot(momentum_range, transmission_prob, label = "Probability at Origin")
    ax.set_xlabel("Momentum")
    ax.set_ylabel("Probability")
    ax.grid(True)
    plt.savefig(path, bbox_inches = "tight")
if __name__ == "__main__":
    transmission_prob_momentum()

