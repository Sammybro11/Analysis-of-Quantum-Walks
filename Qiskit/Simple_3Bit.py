from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np

# Parameters

Nbits = 3
step = 1

qr = QuantumRegister(Nbits, "pos")
coin = QuantumRegister(1, "coin")
cr = ClassicalRegister(Nbits, "Meas")

circuit = QuantumCircuit(qr, coin, cr)

def cnotx(circ, *qbits):
    if len(qbits) > 3:
        # LSE q[0], MSB q[-1]

        circ.crz(np.pi/2, qbits[-2], qbits[-1])
        circ.cu(np.pi/2, 0, 0, 0, qbits[-2], qbits[-1])
        cnotx(circ, *qbits[:-2],qbits[-1])
        circ.cu(-np.pi/2, 0, 0, 0, qbits[-2], qbits[-1])
        cnotx(circ, *qbits[:-2],qbits[-1])
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

def BuildCirc(circ, times):
    for _ in range(times):
        circ.h(coin[0])
        increment_gate(circ, qr, coin[0])
        decrement_gate(circ, qr, coin[0])
        circ.measure(qr[0], cr[2])
        circ.measure(qr[1], cr[1])
        circ.measure(qr[2], cr[0])

def Simulate(circ):
    sim = AerSimulator()
    transpilor = transpile(circ, sim)
    result = sim.run(transpilor, shots = 1024).result()
    return result

BuildCirc(circuit, step)
circuit.draw(output = 'mpl', filename = "qw_results_3bit/circuit.png" )
result_sim = Simulate(circuit)
print("Sim Results: ", result_sim.get_counts(circuit))
