import matplotlib.pyplot as plt
import matplotlib.animation as animation
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


def ProbDist(probability_dist: np.ndarray, t_index: np.ndarray):
    nt, N = probability_dist.shape
    path = Path("Plots/Distribution")

    fig, ax = plt.subplots(figsize = (10, 9))
    for time in t_index:
        ax.plot(np.arange(N), probability_dist[time], label = f"Time: {time}")
    ax.set_xlabel("Lattice")
    ax.set_ylabel("Probability Distribution")
    ax.grid(True)
    ax.legend()
    plt.savefig(path, bbox_inches = "tight")

def ProbDistAnimate(probability_list: np.ndarray, t_series: np.ndarray, name: str, ylim: float):
    N = probability_list[0].shape[1]
    nt = t_series.shape[0]
    path = Path("Plots")

    fig, ax = plt.subplots(figsize = (10, 9))

    x = np.arange(N)

    lines = []
    for i, arr in enumerate(probability_list):
        (ln,) = ax.plot(x, arr[t_series[0]])
        lines.append(ln)


    ax.set_xlabel("Lattice")
    ax.set_ylabel("Probability Distribution")
    ax.set_ylim(0.0, ylim)
    ax.grid(True)

    def init():
        for ln in lines:
            ln.set_ydata(np.zeros_like(x))
        return tuple(lines)

    def update(frame):
        for ln, arr in zip(lines, probability_list):
            ln.set_ydata(arr[frame])
        ax.set_title(f"Time: {frame}")
        return tuple(lines)

    anim = animation.FuncAnimation(fig, update, frames = t_series,
                                   init_func = init, blit = True)

    anim.save(path/ f"animation_{name}.mp4", fps = 10)
