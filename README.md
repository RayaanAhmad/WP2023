# Qubit Calculator
## Summary
Welcome to my qubit calculator, it works as a simple 4-bit addition and subtraction calculator on positive numbers. It operates hybridly, with the inputs and outputs 
(such as the negative flag to indicate whether to read it as a signed or unsigned number) being handle classically, while the operations of the full adder are handled using qubits.
There is a simpler version that operates on 3 bits that can only do addition. To visualize the circuit, there exists a png in the folder of the circuit that gets used.

## Difference in circuit versions
There is a notable difference in how each circuit is created and handled.
Version 1 requires 8 qubits, requiring 3 qubits of each input and 2 auxiliary qubits for the full adder, while version 2 only requries 4 qubits, with 2 qubits for input and 2 auxiliary qubits.
If both the versions operated on the same number of bits (such as 4 bits each), then version 2 would be a deeper circuit as it recycles its input qubits (by resetting and setting a new starting state), which version 1 doesn't need to do
as it has enough qubits for the input. However, this is not a significant increase in depth (at most an increase by 7 for resetting and state an extra 3 times).

## How to run
1) Make sure to have qiskit and qiskit-aer packages downloaded
2) Within the main.py file, change the values of the variables 'valueA', 'valueB', and 'operation'
3) Enjoy your output in the terminal!

For valueA and valueB, use an integer between 0 and 15 (inclusive), and for the operation, choose the character '+' or '-'
If you would like to run the first version of the calculator, uncomment the import for circuit_v1 and its function call, then comment out the import for circuit_v2 and its function call.
The code defaults to using circuit_v2. For the circuit_v1, valueA and valueB are going to be between 0 to 7 (inclusive), but any value outside these ranges will be taken modulo 8.
The output will be in binary form and does require an operation field, it only supports addition.
