from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
import qiskit
from qiskit_aer import AerSimulator

def step_gate(circ, coin, q):
    circ.h(coin[0])
    circ.cx(coin[0], q[1])
    circ.cx(coin[0], q[0])
    circ.x(coin[0])
    circ.cx(coin[0], q[1])

N_STEPS = 6
SHOTS = 1024

coin = QuantumRegister(1, "coin")
pos  = QuantumRegister(2, "pos")
creg = ClassicalRegister(2, "c")
qc = QuantumCircuit(pos, coin, creg)

step_gate(qc, coin, pos)
step_gate(qc, coin, pos)
for i in range(N_STEPS - 2):
    qc.h(coin[0])
    step_gate(qc, coin, pos)

qc.measure(pos[1], creg[0])  # MSB -> bit 0
qc.measure(pos[0], creg[1])  # LSB -> bit 1

print(qc.draw(output="text"))

sim = AerSimulator()
tqc = transpile(qc, sim)
result = sim.run(tqc, shots=SHOTS).result()
print("Final counts:", result.get_counts())
