import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def ProbEvol(times: np.ndarray, region: np.ndarray, labels: list[str] = ["Left", "Between", "Right"]):
    fig, ax = plt.subplots(figsize = (10, 9))
    path = Path("Plots/Evolution.png")

    for i in range(region.shape[0]):
        ax.plot(times, region[i], label = labels[i])

    ax.set_xlabel("Time")
    ax.set_ylabel("Probability")
    ax.set_title("Region Probabilities vs Time")
    ax.legend()
    ax.grid(True)
    plt.savefig(path, bbox_inches = "tight")



def ProbDist(probability_dist: np.ndarray, t_index: int):
    nt, N = probability_dist.shape
    path = Path("Plots/Distribution")

    fig, ax = plt.subplots(figsize = (10, 9))

    ax.plot(np.arange(N), probability_dist[t_index])
    ax.set_xlabel("Lattice")
    ax.set_ylabel("Probability Distribution")
    ax.grid(True)
    plt.savefig(path, bbox_inches = "tight")
