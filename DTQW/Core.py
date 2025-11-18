import numpy as np
import scipy.sparse as sp
from typing import Sequence

class Hamiltonian:
    """
    For DTQW we store the one-step unitary U (2N x 2N sparse matrix)
    in self.Hamiltonian (to match your CTQW naming).
    The basis ordering: index = 2*pos + coin (coin=0,1).
    """
    def __init__(self, Num_sites: int):
        self.N = Num_sites
        # build Hadamard coin blocks (will be used as default coin at each site)
        self._hadamard = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        # default no-defect unitary
        self.Hamiltonian = self._build_unitary(defect_sites={}, as_sparse=True)

    def _build_unitary(self, defect_sites: dict[int, float], as_sparse: bool = True):
        """
        Construct U = S * C_total where C_total is block-diagonal coin operator.
        defect_sites: mapping pos -> phase (radians). At those sites coin = e^{i phi} * H
        """
        N = self.N
        # build block-diagonal coin operator (2N x 2N)
        blocks = []
        for pos in range(N):
            phi = defect_sites.get(pos, 0.0)
            if abs(phi) < 1e-15:
                Cj = self._hadamard
            else:
                Cj = np.exp(1j * phi) * self._hadamard
            blocks.append(sp.csr_matrix(Cj))
        C_total = sp.block_diag(blocks, format='csr')  # 2N x 2N

        # conditional shift S
        N2 = 2 * N
        rows = []
        cols = []
        data = []

        def idx(p, c): return 2 * p + c

        # coin=0 => move right (pos -> pos+1); coin=1 => move left (pos -> pos-1)
        for p in range(N):
            rpos = p + 1
            lpos = p - 1
            # shift right for coin 0
            if 0 <= rpos < N:
                rows.append(idx(rpos, 0)); cols.append(idx(p, 0)); data.append(1.0)
            # shift left for coin 1
            if 0 <= lpos < N:
                rows.append(idx(lpos, 1)); cols.append(idx(p, 1)); data.append(1.0)

        S = sp.csr_matrix((data, (rows, cols)), shape=(N2, N2))
        U = S.dot(C_total)  # 2N x 2N sparse matrix
        return U if as_sparse else U.toarray()

    def addDefects(self, def_sites: list[int], defect_str: float):
        """
        Add phase-defects by rebuilding U with phases at given positions.
        def_sites : list of positions (int)
        defect_str: phase in radians (float). This multiplies the Hadamard at the site by e^{i*defect_str}.
        """
        defect_map = {int(s): float(defect_str) for s in def_sites}
        self.Hamiltonian = self._build_unitary(defect_sites=defect_map, as_sparse=True)


class Wavefunction:
    """
    Produces an initial state vector of length 2N (coin+position).
    If gaussian==False: it creates a localized state at 'center' with equal coin amplitudes.
    If gaussian==True: creates a Gaussian position envelope times e^{i k j}, with coin chosen as right-moving default.
    """
    def __init__(self, gaussian: bool, Num_sites: int, center: int, coin_init: np.ndarray = np.array([1.0, 0.0 + 1.0j], dtype=complex) / np.sqrt(2)):
        self.N = Num_sites
        self.sites = np.arange(self.N)
        # localized at center, equal superposition in coin (normalized)
        psi = np.zeros(2 * self.N, dtype=complex)
        coin_state = coin_init
        psi[2*center + 0] = coin_state[0]
        psi[2*center + 1] = coin_state[1]
        psi /= np.linalg.norm(psi)
        self.psi = psi


class Evolver:
    """
    Evolver accepts the Hamiltonian (unitary) and Wavefunction and evolves by repeated application of U.
    Its run(times) returns (vectors, probability) where:
      - vectors.shape == (nt, 2N) (complex states at requested times)
      - probability.shape == (nt, N) (position probabilities summed over coin)
    """
    def __init__(self, Hamiltonian, Wavefunction):
        self.Hamiltonian = Hamiltonian
        self.Wavefunction = Wavefunction

        self.U = getattr(Hamiltonian, "Hamiltonian")  # sparse 2N x 2N
        self.psi0 = getattr(Wavefunction, "psi")      # length 2N

        # quick checks
        if self.U.shape[0] != 2 * self.Wavefunction.N:
            raise ValueError("Unitary dimension mismatch vs wavefunction length")

    def run(self, times: np.ndarray):
        """
        times: 1D integer-like sequence (e.g., np.arange(0, tmax+1))
        Returns: (vectors, probability)
        """
        times = np.asarray(times, dtype=int)
        if times.ndim != 1 or times.size == 0:
            raise ValueError("Boy that times better be an array")

        nt = times.size
        tmax = int(times[-1])

        N2 = 2 * self.Wavefunction.N
        # iterate step-by-step and capture requested samples (fast enough for moderate tmax).
        vecs = np.zeros((nt, N2), dtype=complex)
        prob = np.zeros((nt, self.Wavefunction.N), dtype=float)

        psi = self.psi0.copy()
        # if time 0 requested, store it
        sample_index = 0
        t_requested = set(int(t) for t in times)

        if 0 in t_requested:
            vecs[sample_index, :] = psi
            # compute position probabilities (sum over coin)
            probs_pos = (np.abs(psi.reshape(-1, 2))**2).sum(axis=1)
            prob[sample_index, :] = probs_pos
            sample_index += 1

        # apply unitary for steps 1..tmax
        for t in range(1, tmax + 1):
            psi = self.U.dot(psi)
            if t in t_requested:
                vecs[sample_index, :] = psi
                probs_pos = (np.abs(psi.reshape(-1, 2))**2).sum(axis=1)
                prob[sample_index, :] = probs_pos
                sample_index += 1

        return vecs, prob
