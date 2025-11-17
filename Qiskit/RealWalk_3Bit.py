# Qiskit 1.x — 3-bit position walk with increment/decrement gates

import os, json
import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit_ibm_runtime import QiskitRuntimeService

# method from Qiskit tutorial on Quantum Walks
def cnotx(circ, *qbits):
    if len(qbits) > 3:
        circ.crz(np.pi/2, qbits[-2], qbits[-1])
        circ.cu(np.pi/2, 0, 0, 0, qbits[-2], qbits[-1])
        cnotx(circ, *qbits[:-2], qbits[-1])
        circ.cu(-np.pi/2, 0, 0, 0, qbits[-2], qbits[-1])
        cnotx(circ, *qbits[:-2], qbits[-1])
        circ.crz(-np.pi/2, qbits[-2], qbits[-1])

    elif len(qbits) == 3:
        circ.ccx(*qbits)

    elif len(qbits) == 2:
        circ.cx(*qbits)


def increment_gate(circ, q, coin):
    cnotx(circ, coin, q[2], q[1], q[0])
    cnotx(circ, coin, q[2], q[1])
    cnotx(circ, coin, q[2])


def decrement_gate(circ, q, coin):
    circ.x(coin)
    circ.x(q[2])
    circ.x(q[1])
    cnotx(circ, coin, q[2], q[1], q[0])
    circ.x(q[1])
    cnotx(circ, coin, q[2], q[1])
    circ.x(q[2])
    cnotx(circ, coin, q[2])
    circ.x(coin)
    circ.barrier()

def get_gates(tqc):
    return set(tqc.count_ops().keys())

def get_qbits(tqc):
    used = set()
    for instr in tqc.data:
        inst = instr.operation
        for q in instr.qubits:
            used.add(q._index)
    return used

def build_walk_3bit(n_steps):
    qr = QuantumRegister(3, "pos")
    coin = QuantumRegister(1, "coin")
    cr = ClassicalRegister(3, "Meas")

    qc = QuantumCircuit(qr, coin, cr)

    for _ in range(n_steps):
        qc.h(coin[0])
        increment_gate(qc, qr, coin[0])
        decrement_gate(qc, qr, coin[0])

    qc.measure(qr[0], cr[2])   # LSB → rightmost classical bit
    qc.measure(qr[1], cr[1])
    qc.measure(qr[2], cr[0])   # MSB → left classical bit

    outcomes = [format(i, "03b") for i in range(8)]
    return qc, outcomes



def counts_to_prob(counts, outcomes):
    total = sum(counts.values()) if counts else 1
    return np.array([counts.get(o, 0) / total for o in outcomes], float)


def hellinger(p, q):
    return np.linalg.norm(np.sqrt(p) - np.sqrt(q))


def hellinger_fidelity(p, q):
    H = hellinger(p, q)
    return (1 - H**2)**2   # used in DTQW papers


def ideal_counts(qc, outcomes, shots=20000):
    sim = AerSimulator()
    tq = transpile(qc, sim)
    result = sim.run(tq, shots=shots).result()
    c = result.get_counts()
    for o in outcomes:
        c.setdefault(o, 0)
    return c


def noisy_counts(qc, outcomes, shots, noise_model):
    sim = AerSimulator()
    tq = transpile(qc, sim)
    result = sim.run(tq, noise_model=noise_model, shots=shots).result()
    c = result.get_counts()
    for o in outcomes:
        c.setdefault(o, 0)
    return c

def make_noise(backend_name):
    service = QiskitRuntimeService()
    backend = service.backend(backend_name)

    noise_model = NoiseModel.from_backend(backend)
    return noise_model, backend


def make_noise_manual():
    nm = NoiseModel()

    # 1-qubit gate noise
    nm.add_all_qubit_quantum_error(depolarizing_error(0.001, 1), ['h', 'x'])

    # 2-qubit gates noise
    nm.add_all_qubit_quantum_error(depolarizing_error(0.01, 2), ['cx', 'cu', 'crz'])

    # 3-qubit CCX noise
    nm.add_all_qubit_quantum_error(depolarizing_error(0.02, 3), ['ccx'])

    return nm

def extract_backend_errors(backend, tqc):
    props = backend.properties()
    used_gates = get_gates(tqc)
    used_qubits = get_qbits(tqc)
    print(used_gates)

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


def run_experiments(step_list, shots=2048, noisy=True):
    qc_temp, _ = build_walk_3bit(step_list[-1])
    # print(qc_temp.draw(output = "text"))
    print(qc_temp.count_ops())

    os.makedirs("qw_results_3bit/", exist_ok = True)
    if noisy:
        noise_model, backend = make_noise("ibm_marrakesh")
        tqc = transpile(qc_temp, backend)

        backend_errors = extract_backend_errors(backend, tqc)
    else:
        noise_model, backend, backend_errors = None, None, {}
    all_results = []

    for steps in step_list:
        qc, outcomes = build_walk_3bit(steps)

        c_ideal = ideal_counts(qc, outcomes, shots)
        p_ideal = counts_to_prob(c_ideal, outcomes)

        if noisy:
            c_noisy = noisy_counts(qc, outcomes, shots, noise_model)
        else:
            c_noisy = {o: 0 for o in outcomes}
        p_noisy = counts_to_prob(c_noisy, outcomes)

        H = hellinger(p_ideal, p_noisy)

        print(f"steps={steps}   Hellinger={H:.6f}")

        all_results.append({
            "steps": steps,
            "counts_ideal": c_ideal,
            "counts_noisy": c_noisy,
            "Hellinger": float(H)
        })

    full_output = {
        "backend_name": backend.name if backend else None,
        "backend_errors": backend_errors,
        "results": all_results
    }

    os.makedirs("qw_results_3bit", exist_ok=True)

    with open("qw_results_3bit/results.json", "w") as f:
        json.dump(full_output, f, indent=2)

    print("Saved results → qw_results_3bit/")
    return all_results

if __name__ == "__main__":
    steps_to_run = [1, 2, 3, 4, 5, 6, 7, 8]
    run_experiments(steps_to_run, shots=1024, noisy=True)
