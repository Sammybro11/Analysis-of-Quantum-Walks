import numpy as np
import scipy.sparse as sp
from typing import Sequence

class Hamiltonian:
    def __init__(self, Num_sites: int):
        self.N = Num_sites
        main = 2.0 * np.ones(self.N)                   # main diagonal
        off_diag = -1.0 * np.ones(self.N - 1)

        self.Hamiltonian = np.diag(main, 0) + np.diag(off_diag, -1) + np.diag(off_diag, +1)

    def addDefects(self, def_sites: list[int], defect_str: list[float]):
        Defected_Hamiltonian = self.Hamiltonian.copy().astype(complex)
        for site, strength in zip(def_sites, defect_str):
            Defected_Hamiltonian[int(site), int(site)] += strength
        self.Hamiltonian = Defected_Hamiltonian

class Wavefunction:
    def __init__(self, gaussian: bool, Num_sites: int, center: int, spread: float = 15.0, momentum: float = 1.0 ):
        if gaussian:
            if momentum >= np.pi:
                raise ValueError("Momentum can't be more than pi")

            self.N = Num_sites
            self.sites = np.arange(self.N)
            self.psi = np.exp(- (self.sites - center)**2 / (2 * spread**2)) * np.exp(1j * momentum * self.sites)
            self.psi /= np.linalg.norm(self.psi)
        else:
            self.N = Num_sites
            self.psi = np.zeros(self.N, dtype = complex)
            self.psi[center] = 1.0 # Total Prob 1 at point

class Evolver:
    def __init__(self, Hamiltonian, Wavefunction):
        self.Hamiltonian = Hamiltonian
        self.Wavefunction = Wavefunction

        self.H = getattr(Hamiltonian, "Hamiltonian")
        self.psi = getattr(Wavefunction, "psi")

    def run(self, times):
        times = np.asarray(times)
        if times.ndim != 1 or times.size == 0:
            raise ValueError("Boy that times better be an array")

        nt = times.size

        vectors = sp.linalg.expm_multiply(-1j * self.H, self.psi, start = times[0], stop = times[-1], num = nt)

        vectors = np.asarray(vectors)
        probability = np.abs(vectors)**2

        return vectors, probability

    # @staticmethod
    # def region_prob_double(vectors: np.ndarray, site0: int, site1: int, buffer: int):
    #     probs = Evolver.probability(vectors)
    #     nt, N = probs.shape
    #
    #     left_end = max(0, site0 - buffer)
    #     right_start = min(N, site1  + buffer)
    #
    #     left_idx = np.arange(0, left_end, dtype = int)
    #     between_idx = np.arange(max(0, site0 + 1), min(N, site1 - 1))
    #     right_idx = np.arange(right_start, N, dtype = int)
    #
    #     prob_left = np.sum(probs[:, left_idx], axis = 1)
    #     prob_between = np.sum(probs[:, between_idx], axis = 1)
    #     prob_right = np.sum(probs[:, right_idx], axis = 1)
    #
    #     return np.array([prob_left, prob_between, prob_right])
    #
    # @staticmethod
    # def region_prob(vectors: np.ndarray, site0: int, buffer: int):
    #     probs = Evolver.probability(vectors)
    #     nt, N = probs.shape
    #
    #     left_idx = np.arange(0, site0 - buffer, dtype = int)
    #     right_idx = np.arange(site0 + 1, N, dtype = int)
    #
    #     prob_left = np.sum(probs[:, left_idx], axis = 1)
    #     prob_right = np.sum(probs[:, right_idx], axis = 1)
    #
    #     return np.array([prob_left, prob_right])
    #
    # def run_analyze(self, times, site0: int, buffer: int):
    #     vectors = Evolver.run(self, times)
    #     probs = Evolver.probability(vectors)
    #     regions = Evolver.region_prob(vectors, site0, buffer)
    #
    #     return vectors, probs, regions
