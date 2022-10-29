from secret import get_01_flag_str
from qiskit import QuantumCircuit, Aer, assemble
from Crypto.Random import random
import sys


def get_circuit_map(token, filename):
    flag_01 = get_01_flag_str(token)
    len_flag = len(flag_01)         # 16 * 8 = 128

    print("flag_01:", flag_01)

    obfuscation_type_1 = 10
    obfuscation_type_2 = 5
    classic_reg_num = len_flag      # 经典寄存器的数量 128
    quantum_reg_num = len_flag + 1  # 量子寄存器的数量 129
    aux_qubit_index = len_flag      # 辅助qubit的下标 128

    # step 1
    bv_circuit = QuantumCircuit(quantum_reg_num, classic_reg_num)
    bv_circuit.x(len_flag)
    for i in range(quantum_reg_num):
        bv_circuit.h(i)

    bv_circuit.barrier()

    # step 1.5 (optional) obfuscation

    obfuscation_index_1 = random.sample(range(quantum_reg_num - 1),
                                        obfuscation_type_1)

    obfuscation_index_2 = random.sample(range(quantum_reg_num - 1),
                                        obfuscation_type_2)

    # step 2
    flag_01 = flag_01[::-1]
    for i in range(len_flag):
        if i in obfuscation_index_1:
            bv_circuit.x(i)
        if i in obfuscation_index_2:
            bv_circuit.z(i)
        if flag_01[i] == '1':
            bv_circuit.cx(i, aux_qubit_index)
        if (quantum_reg_num - 2 - i) in obfuscation_index_2:
            bv_circuit.z(quantum_reg_num - 2 - i)

    for i in range(len_flag):
        if i in obfuscation_index_1:
            bv_circuit.x(i)

    bv_circuit.barrier()

    # step 3
    for i in range(quantum_reg_num - 1):
        bv_circuit.h(i)

    bv_circuit.draw(output="mpl", filename=filename, interactive=False,
                    initial_state=True, vertical_compression="high",
                    fold=100, scale=0.8, justify="left")

    return bv_circuit


if __name__ == "__main__":
    if len(sys.argv) != 3:
        valid_token = "<fill in a valid token here>"

        flag_01 = get_01_flag_str(valid_token)
        print(flag_01)

        circuit = get_circuit_map(valid_token,
                                  "./static/output/test.png")
        for i in range(128):
            circuit.measure(i, i)

        aer_sim = Aer.get_backend('aer_simulator')
        shots = 100
        qobj = assemble(circuit)
        results = aer_sim.run(qobj, shots=shots).result()
        answer = results.get_counts()
        print(answer)
        assert (len(answer) == 1)
        assert (list(answer.keys())[0] == flag_01)
    else:
        token = sys.argv[1]
        filename = sys.argv[2]
        print(token, filename)
        get_circuit_map(token, filename)
