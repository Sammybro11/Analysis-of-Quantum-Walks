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


def MomentumDistAnimate(vector_list: np.ndarray, t_series: np.ndarray, name: str):
    path = Path("Plots")
    fig, ax = plt.subplots(figsize=(10, 9))

    n_scenarios = vector_list.shape[0]
    nt = vector_list.shape[1]
    M = vector_list.shape[2]

    # detect CTQW vs DTQW: if M is even and >= 2, assume DTQW with coin dim 2
    if M % 2 == 0 and (M // 2) * 2 == M and n_scenarios >= 0:
        is_dtqw = True
        N = M // 2
    else:
        is_dtqw = False
        N = M

    # build k axis (centered)
    k = np.fft.fftshift(np.fft.fftfreq(N, d=1) * 2 * np.pi)

    lines = []
    x = k

    # initialize a line for each scenario
    for i in range(n_scenarios):
        psi_t0 = vector_list[i, t_series[0]]    # complex amplitude vector
        # project to position amplitude if DTQW
        if is_dtqw:
            psi_pos = psi_t0.reshape(N, 2).sum(axis=1)   # sum coin amplitudes -> position amplitude
        else:
            psi_pos = psi_t0
        psi_k = np.fft.fftshift(np.fft.fft(psi_pos))
        Pk = np.abs(psi_k)**2 / N
        (ln,) = ax.plot(x, Pk)
        lines.append(ln)

    ax.set_xlabel("k")
    ax.set_ylabel("Momentum Probability |ψ(k)|²")
    ax.grid(True)

    def init():
        for ln in lines:
            ln.set_ydata(np.zeros_like(x))
        return tuple(lines)

    def update(frame):
        for ln, arr in zip(lines, vector_list):
            psi_t = arr[frame]
            if is_dtqw:
                psi_pos = psi_t.reshape(N, 2).sum(axis=1)
            else:
                psi_pos = psi_t
            psi_k = np.fft.fftshift(np.fft.fft(psi_pos))
            Pk = np.abs(psi_k)**2 / N
            ln.set_ydata(Pk)
        ax.set_title(f"Time: {frame}")
        return tuple(lines)

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=t_series,
        init_func=init,
        blit=True
    )

    anim.save(path / f"momentum_animation_{name}.mp4", fps=10)
