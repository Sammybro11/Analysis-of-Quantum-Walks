# Qiskit 1.x DTQW with noisy/ideal counts + Hellinger distance

import json, os
import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService

def step_gate(circ, coin, q):
    circ.h(coin[0])
    circ.cx(coin[0], q[1])
    circ.cx(coin[0], q[0])
    circ.x(coin[0])
    circ.cx(coin[0], q[1])


def build_walk(n_steps):
    coin = QuantumRegister(1, "coin")
    pos  = QuantumRegister(2, "pos")
    creg = ClassicalRegister(2, "c")

    qc = QuantumCircuit(pos, coin, creg)

    step_gate(qc, coin, pos)
    step_gate(qc, coin, pos)

    for _ in range(n_steps - 2):
        qc.h(coin[0])
        step_gate(qc, coin, pos)

    qc.measure(pos[1], creg[0])  # MSB
    qc.measure(pos[0], creg[1])  # LSB

    return qc, ['00', '01', '10', '11']

def get_used_gates_from_tqc(tqc):
    return set(tqc.count_ops().keys())

def get_used_qubits(tqc):
    used = set()
    for instr in tqc.data:
        inst = instr.operation
        for q in instr.qubits:
            used.add(q._index)
    return used

def hellinger(p, q):
    """Physics convention: no 1/sqrt(2)."""
    return np.linalg.norm(np.sqrt(p) - np.sqrt(q))

# Not using right now might use later
def hellinger_fidelity(p, q):
    """Paper’s definition: F = (1 - H^2)^2."""
    H = hellinger(p, q)
    return (1 - H**2)**2


def counts_to_prob_vector(counts, outcomes):
    total = sum(counts.values()) if counts else 1
    return np.array([counts.get(o, 0) / total for o in outcomes], dtype=float)


def ideal_counts(qc, outcomes, shots=20000):
    sim = AerSimulator()
    tq = transpile(qc, sim)
    result = sim.run(tq, shots=shots).result()
    counts = result.get_counts()
    for o in outcomes:
        counts.setdefault(o, 0)
    return counts


def noisy_counts(qc, outcomes, shots, noise_model):
    sim = AerSimulator()
    tq = transpile(qc, sim)
    result = sim.run(tq, noise_model=noise_model, shots=shots).result()
    counts = result.get_counts()
    for o in outcomes:
        counts.setdefault(o, 0)
    return counts


def make_noise(backend_name):
    service = QiskitRuntimeService()
    backend = service.backend(backend_name)

    noise_model = NoiseModel.from_backend(backend)
    return noise_model, backend

def extract_backend_errors(backend, tqc):
    props = backend.properties()
    used_gates  = get_used_gates_from_tqc(tqc)
    used_qubits = get_used_qubits(tqc)

    data = {"gates": {}}

    for gate in props.gates:
        gname = gate.gate
        qr    = tuple(gate.qubits)

        if gname not in used_gates:
            continue

        if not all(q in used_qubits for q in qr):
            continue

        for p in gate.parameters:
            if p.name == "gate_error":
                key = f"{gname}{qr}"
                data["gates"][key] = float(p.value)

    return data

def run_experiments(step_list, shots=2048, noisy=True, real=False):
    qc_temp, _ = build_walk(step_list[-1])
    print(qc_temp.count_ops())

    os.makedirs("qw_results_2bit/", exist_ok=True)
    OUTCOMES = ['00', '01', '10', '11']
    if noisy:
        noise_model, backend = make_noise("ibm_marrakesh")
        tqc = transpile(qc_temp, backend)

        backend_errors = extract_backend_errors(backend, tqc)
    else:
        noise_model, backend, backend_errors = None, None, {}
    all_results = []

    for n in step_list:

        qc, _ = build_walk(n)

        counts_ideal = ideal_counts(qc, OUTCOMES, shots)
        p_ideal = counts_to_prob_vector(counts_ideal, OUTCOMES)

        if noisy:
            counts_noisy = noisy_counts(qc, OUTCOMES, shots, noise_model)
        else:
            counts_noisy = {o: 0 for o in OUTCOMES}
        p_noisy = counts_to_prob_vector(counts_noisy, OUTCOMES)

        H = hellinger(p_ideal, p_noisy)

        print(f"steps={n}   Hellinger={H:.6f}")


        all_results.append({
            "steps": n,
            "counts_ideal": counts_ideal,
            "counts_noisy": counts_noisy,
            "Hellinger": float(H)
        })

    full_output = {
        "backend_name": backend.name if backend else None,
        "backend_errors": backend_errors,
        "results": all_results
    }

    with open("qw_results_2bit/results.json", "w") as f:
        json.dump(full_output, f, indent=2)

    print("Saved results → qw_results_2bit/")

    return all_results

if __name__ == "__main__":
    steps = [0, 1, 2, 3, 4, 5, 6]
    run_experiments(steps, shots=1024, noisy=True, real=False)
