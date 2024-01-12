# Qubit Calculator V2
#   Qubits = 4
#   Depth = 34
# Supports addition and subtraction

from qiskit import QuantumCircuit, Aer


# Takes number and returns the 2's complement 4-bit binary
# Inputs:
#   num - integer from -8 to 7 : int
# Returns:
#   binary - resulting 4 bit representation : list
# Credits: Written by Nashwaan Ahmad
def binary_rep(num):
    binary = [0, 0, 0, 0]
    if num < 0:
        binary[0] = 1
        num = num + 8

    index = len(binary) - 1
    while num:
        if num & 1:
            binary[index] = 1
        index -= 1
        num >>= 1
    return binary


# The circuitry for a full adder
# Inputs:
#   qc - the circuit we are adding upon, must have 8 qubits : QuantumCircuit
#   bitA - position of qubitA (index 0-2) : int
#   bitB - position of qubitB (= bitA + 3) : int
# Returns:
#   qc - modified version of the circuit given to us : QuantumCircuit
def full_adder(qc, bitA, bitB):
    cIn = 2
    memory = 3

    qc.ccx(bitA, cIn, memory)
    qc.ccx(bitB, cIn, memory)
    qc.ccx(bitA, bitB, memory)

    qc.cx(bitB, bitA)
    qc.cx(cIn, bitA)

    qc.reset(cIn)
    qc.cx(memory, cIn)
    qc.reset(memory)
    return qc


# Create a quantum circuit acting as a 3bit full adder
# Inputs:
#   A - integer from 0 to 15 : int
#   B - integer from 0 to 15 : int
#   op - '+' or '-' operation : char
# Returns:
#   output - resulting integer from -8 to 15 : int
#   On error, returns None
def quantum_circuit(A, B, op):
    # Safety check !!
    if (not (-1 < A < 16)) or (not (-1 < B < 16)) or (op != '+' and op != '-'):
        return None

    # Create circuit with 2 operating qubits, 1 carry qubit, 1 memory qubit, 4 bits for output, 1 bit overflow
    circuit = QuantumCircuit(4, 5)

    # Convert A,B to binary strings
    char_bin_A = binary_rep(A)
    char_bin_B = binary_rep(B)
    char_bin_A.reverse()
    char_bin_B.reverse()

    # State prep and operands on our bits
    if op == '-':
        for x in range(4):
            if char_bin_B[x] == 1:
                char_bin_B[x] = 0
            else:
                char_bin_B[x] = 1

        circuit.x(2)

    for x in range(4):
        circuit.reset([0, 1])
        if char_bin_A[x] == 1:
            circuit.x(0)
        if char_bin_B[x] == 1:
            circuit.x(1)

        circuit = full_adder(circuit, 0, 1)
        circuit.measure(0, x)

    circuit.measure(2, 4)

    # Acquiring output
    backend = Aer.get_backend('aer_simulator')
    result = backend.run(circuit, shots=25).result()
    counts = result.get_counts(circuit)

    output = list(counts.keys())[0]
    num_output = int(output[1:], 2)

    # print(output)
    if (op == '-') and (output[0] == '0'):
        print("Value =", num_output - 16)
    else:
        print("Value =", num_output)
    # print("Depth =", circuit.depth())

    # Draw our circuit for analysis
    circuit_img = circuit.draw(output="mpl", style="iqp")
    circuit_img.savefig("circuitv2_drawing.png")


# Testing
# quantum_circuit(5, 3, '-')
