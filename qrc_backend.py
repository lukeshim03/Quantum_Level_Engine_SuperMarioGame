import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_braket_provider import BraketProvider

N_QUBITS = 6
N_SHOTS = 1024
USE_HARDWARE = os.getenv("QRC_USE_HARDWARE", "false").lower() == "true"

def get_backend():
    if USE_HARDWARE:
        # IonQ hardware is accessed via cloud providers (e.g., AWS Braket)
        provider = BraketProvider()
        return provider.get_backend("Aria 1")
    return AerSimulator(method="statevector")

def build_reservoir_circuit(tile_sequence: list[float]) -> QuantumCircuit:
    """
    Encode tile sequence into the 6-qubit quantum reservoir.
    Architecture:
      1. Ry(θ_i)      — encode tile value as rotation angle
      2. CNOT ladder  — entangle adjacent qubits (ring topology)
      3. Ry(π/4)      — mixing rotations for reservoir dynamics
      4. Measure all  — extract probability vector
    """
    qc = QuantumCircuit(N_QUBITS, N_QUBITS)

    # Layer 1 — encode tile values as rotation angles
    for i, val in enumerate(tile_sequence):
        theta = float(val) * np.pi      # map [0,1] → [0, π]
        qc.ry(theta, i)

    # Layer 2 — CNOT ladder for entanglement
    for i in range(N_QUBITS):
        qc.cx(i, (i + 1) % N_QUBITS)

    # Layer 3 — mixing rotations
    for i in range(N_QUBITS):
        qc.ry(np.pi / 4, i)

    qc.measure(list(range(N_QUBITS)), list(range(N_QUBITS)))
    return qc

def run_qrc_circuit(circuit: QuantumCircuit, shots: int = N_SHOTS) -> dict:
    backend = get_backend()
    job = backend.run(circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(circuit)
    return counts
