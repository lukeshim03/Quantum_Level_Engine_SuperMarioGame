import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_braket_provider import BraketProvider

N_QUBITS = 6
USE_HARDWARE = os.getenv("BOSS_USE_HARDWARE", "false").lower() == "true"

def get_boss_backend():
    if USE_HARDWARE:
        # IonQ hardware is accessed via cloud providers (e.g., AWS Braket)
        provider = BraketProvider()
        return provider.get_backend("Aria 1")
    return AerSimulator(method="statevector")

def build_boss_circuit(boss_hp_percentage: float) -> QuantumCircuit:
    """
    Creates a quantum circuit for the boss fight.
    Entanglement strength is inversely proportional to boss HP.
    Full HP (1.0) -> Low entanglement (more chaotic/unpredictable collapses)
    Low HP (0.1) -> High entanglement (more orderly/predictable collapses)
    """
    qc = QuantumCircuit(N_QUBITS, N_QUBITS)
    
    # Base superposition
    for i in range(N_QUBITS):
        qc.h(i)
        
    # Entanglement layer controlled by boss HP
    # We map HP [0, 1] to an angle [pi, 0] for the CRX gate
    # Lower HP means stronger rotation (more entanglement)
    entanglement_angle = (1.0 - boss_hp_percentage) * np.pi
    
    for i in range(N_QUBITS - 1):
        qc.crx(entanglement_angle, i, i + 1)
        
    # Close the ring
    qc.crx(entanglement_angle, N_QUBITS - 1, 0)
    
    qc.measure(list(range(N_QUBITS)), list(range(N_QUBITS)))
    return qc

def trigger_boss_collapse(boss_hp_percentage: float) -> str:
    """
    Executes the boss circuit and returns the dominant bitstring.
    This bitstring determines which level zone collapses.
    """
    circuit = build_boss_circuit(boss_hp_percentage)
    backend = get_boss_backend()
    
    # For boss events, we might use fewer shots for faster response if on hardware,
    # but 100 is a reasonable balance for finding a dominant state.
    job = backend.run(circuit, shots=100)
    result = job.result()
    counts = result.get_counts(circuit)
    
    # Find the most frequent bitstring
    dominant_bitstring = max(counts, key=counts.get)
    return dominant_bitstring

def map_bitstring_to_zone(bitstring: str) -> int:
    """
    Maps a 6-qubit bitstring to one of 6 level zones.
    A simple approach is counting the number of '1's.
    """
    return bitstring.count('1')
