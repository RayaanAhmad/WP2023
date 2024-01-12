# Qubit Calculator V1
#   Qubits = 8
#   Depth = 25
# Only supports addition

from qiskit import QuantumCircuit, Aer


# Takes number and returns the 3 bit representation
# Inputs:
#   num - integer from 0-7 (3 bits) : int
# Returns:
#   binary - resulting 3 bit representation : list
def three_bit_binary(num):
    binary = []
    bin_string = str(bin(num))

    for c in range(2, len(bin_string)):
        binary.append(int(bin_string[c]))

    # Padding up to 3 bits
    while len(binary) != 3:
        binary.insert(0, 0)
    return binary


# The circuitry for a full adder
# Inputs:
#   qc - the circuit we are adding upon, must have 8 qubits : QuantumCircuit
#   bitA - position of qubitA (index 0-2) : int
#   bitB - position of qubitB (= bitA + 3) : int
# Returns:
#   qc - modified version of the circuit given to us : QuantumCircuit
def full_adder(qc, bitA, bitB):
    cIn = 6
    memory = 7

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
#   A - integer from 0-7 : int
#   B - integer from 0-7 : int
# Returns:
#   output - resulting integer from 0-7 (3 bits) : int
def quantum_circuit(A, B):
    # Safety check !!
    A = A % 8
    B = B % 8

    # Create circuit with 6 input qubits, 1 carry qubit, 1 memory qubit, and 3 bits for output
    circuit = QuantumCircuit(8, 3)

    # Convert A,B to binary strings
    char_bin_A = three_bit_binary(A)
    char_bin_B = three_bit_binary(B)
    char_bin_A.reverse()
    char_bin_B.reverse()

    # Initialize our states
    for x in range(3):
        if char_bin_A[x] == 1:
            circuit.x(x)
        if char_bin_B[x] == 1:
            circuit.x(x + 3)

    # Operands on our bits
    for x in range(3):
        circuit = full_adder(circuit, x, x + 3)

    circuit.measure([0, 1, 2], [0, 1, 2])

    # Acquiring output
    backend = Aer.get_backend('aer_simulator')
    result = backend.run(circuit, shots=25).result()
    counts = result.get_counts(circuit)
    print(counts)
    print("Depth = ", circuit.depth())

    # Draw our circuit for analysis
    circuit_img = circuit.draw(output="mpl", style="iqp")
    circuit_img.savefig("circuitv1_drawing.png")


# Testing
# quantum_circuit(3, 5)
