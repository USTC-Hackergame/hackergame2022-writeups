from qiskit import QuantumCircuit, assemble, Aer
import matplotlib.pyplot as plt

qc = QuantumCircuit(129, 128)
for i in range(128):
    qc.h(i)

qc.x(128)
qc.h(128)
qc.barrier()
qc.cx(0, 128)

for i in 1, 8, 9, 33, 64, 67, 96, 117, 125:
    qc.x(i)

for i in 62, 84, 98, 102, 105:
    qc.z(i)

qc.x(1)
qc.cx(2, 128)

for i in 8, 64, 67, 84:
    qc.x(i)

for i in 62, 98, 102, 105:
    qc.z(i)

qc.cx(3, 128)
qc.z(84)

qc.cx(4, 128)
qc.cx(5, 128)
qc.cx(6, 128)
qc.cx(9, 128)

qc.x(9)

for i in 12, 13, 17, 21, 22, 24, 25, 29, 30, 33:
    qc.cx(i, 128)

qc.x(33)
for i in 34, 36, 37, 41, 44, 45, 52, 53, 56, 60, 61, 66, 69, 70, 72, 74, 76, 77, 83, 84:
    qc.cx(i, 128)

qc.x(84)
for i in 85, 88, 89, 91, 92, 93, 94, 96:
    qc.cx(i, 128)

qc.x(96)
for i in 97, 98, 101, 102, 104, 109, 110, 114, 115, 117:
    qc.cx(i, 128)

qc.x(117)
for i in 118, 121, 122, 125:
    qc.cx(i, 128)

qc.x(125)
qc.cx(126, 128)

qc.barrier()
for i in range(128):
    qc.h(i)

qc.draw(output="mpl", filename="out.png", initial_state=True, fold=-1)

sim = Aer.get_backend('aer_simulator')

# measure, get result
qc.measure_all()
result = sim.run(qc).result()
counts = result.get_counts()
print(counts)
