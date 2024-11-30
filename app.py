import streamlit as st
import numpy as np
import qiskit
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt

def quantum_coin_flip():
    """
    Simulate a quantum coin flip using a Hadamard gate
    """
    # Create a quantum circuit with 1 qubit and 1 classical bit
    qc = QuantumCircuit(1, 1)
    
    # Apply Hadamard gate to create superposition
    qc.h(0)
    
    # Measure the qubit
    qc.measure(0, 0)
    
    # Run the simulation
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    return counts

def quantum_teleportation_demo():
    """
    Demonstrate quantum teleportation protocol
    """
    # Create a quantum circuit with 3 qubits and 2 classical bits
    qc = QuantumCircuit(3, 2)
    
    # Prepare entangled pair (Bell state)
    qc.h(1)
    qc.cx(1, 2)
    
    # Prepare arbitrary state on first qubit
    qc.ry(np.pi/4, 0)
    
    # Teleportation protocol
    qc.cx(0, 1)
    qc.h(0)
    
    qc.measure([0, 1], [0, 1])
    
    # Conditional corrections
    qc.cx(1, 2)
    qc.cz(0, 2)
    
    return qc

def main():
    st.title("Quantum Computing Playground")
    
    # Sidebar for navigation
    app_mode = st.sidebar.selectbox("Choose Quantum Experiment", 
        [
            "Quantum Coin Flip", 
            "Quantum Teleportation", 
            "Bloch Sphere Visualization",
            "Bell State Measurement"
        ]
    )
    
    if app_mode == "Quantum Coin Flip":
        st.header("Quantum Coin Flip Simulation")
        st.write("This demonstrates a quantum coin flip using a Hadamard gate")
        
        if st.button("Run Quantum Coin Flip"):
            counts = quantum_coin_flip()
            st.write("Measurement Results:")
            st.bar_chart(counts)
    
    elif app_mode == "Quantum Teleportation":
        st.header("Quantum Teleportation Protocol")
        st.write("Demonstrates the quantum teleportation circuit")
        
        if st.button("Generate Teleportation Circuit"):
            teleport_circuit = quantum_teleportation_demo()
            st.write("Quantum Teleportation Circuit:")
            st.code(teleport_circuit)
    
    elif app_mode == "Bloch Sphere Visualization":
        st.header("Bloch Sphere Visualization")
        
        # Qubit state selection
        theta = st.slider("Rotation Angle (θ)", 0.0, np.pi, np.pi/2)
        phi = st.slider("Rotation Angle (φ)", 0.0, 2*np.pi, 0.0)
        
        # Create a quantum state
        qc = QuantumCircuit(1)
        qc.ry(theta, 0)
        qc.rz(phi, 0)
        
        # Get statevector
        backend = Aer.get_backend('statevector_simulator')
        job = execute(qc, backend)
        statevector = job.result().get_statevector()
        
        # Plot Bloch Sphere
        fig, ax = plt.subplots()
        plot_bloch_multivector(statevector)
        st.pyplot(fig)
    
    elif app_mode == "Bell State Measurement":
        st.header("Bell State Creation")
        
        st.write("Creating a maximally entangled Bell state")
        
        # Create Bell state circuit
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0,1], [0,1])
        
        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1000)
        result = job.result()
        counts = result.get_counts(qc)
        
        st.write("Bell State Measurement Results:")
        st.bar_chart(counts)

if __name__ == "__main__":
    main()
