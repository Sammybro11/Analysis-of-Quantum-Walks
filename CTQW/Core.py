import numpy as np
import scipy.sparse as sp
from typing import Sequence

class Hamiltonian:
    def __init__(self, Num_sites: int):
        self.N = Num_sites
        main = 2.0 * np.ones(self.N)                   # main diagonal
        off_diag = -1.0 * np.ones(self.N - 1)
        offsets = [1, 0, -1]

        self.Hamiltonian = sp.diags([off_diag, main, off_diag], offsets, format="csr")

    def addDefects(self, def_sites: list[int], defect_str: float):
        Defected_Hamiltonian = self.Hamiltonian.copy().astype(complex)
        for site in def_sites:
            Defected_Hamiltonian[site, site] += defect_str
        self.Hamiltonian = Defected_Hamiltonian

class Wavefunction:
    def __init__(self, Num_sites: int, center: float, spread: float, momentum: float ):
        if momentum >= np.pi:
            raise ValueError("Momentum can't be more than pi")

        self.N = Num_sites
        self.sites = np.arange(self.N)
        self.psi = np.exp(- (self.sites - center)**2 / (2 * spread**2)) * np.exp(1j * momentum * self.sites)
        self.psi /= np.linalg.norm(self.psi)

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
        print(vectors.shape)

        return vectors

    @staticmethod
    def probability(vectors: np.ndarray):
        return np.abs(vectors)**2

    @staticmethod
    def region_prob(vectors: np.ndarray, site0: int, site1: int, buffer: int):
        probs = Evolver.probability(vectors)
        nt, N = probs.shape

        left_end = max(0, site0 - buffer)
        right_start = min(N, site1  + buffer)

        left_idx = np.arange(0, left_end, dtype = int)
        between_idx = np.arange(max(0, site0 + 1), min(N, site1 - 1))
        right_idx = np.arange(right_start, N, dtype = int)

        prob_left = np.sum(probs[:, left_idx], axis = 1)
        prob_between = np.sum(probs[:, between_idx], axis = 1)
        prob_right = np.sum(probs[:, right_idx], axis = 1)

        return np.array([prob_left, prob_between, prob_right])

    def run_analyze(self, times, site0: int, site1: int, buffer: int):
        vectors = Evolver.run(self, times)
        probs = Evolver.probability(vectors)
        regions = Evolver.region_prob(vectors, site0, site1, buffer)

        return vectors, probs, regions
