import pennylane as qml
from pennylane.math import reduce_dm, partial_trace
from pennylane import numpy as np

dev = qml.device('default.mixed', wires=3)
@qml.qnode(dev)
def GHZ():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    return qml.density_matrix(wires=range(3))

def measure_and_update_density_matrix(rho, input):
  size = len(rho)//2
  
  if input == 0:
    
    # Eigenstates of Pauli X observable
    pauli_x_plus = np.array([1, 1]) / np.sqrt(2)
    pauli_x_minus = np.array([1, -1]) / np.sqrt(2)
    
    # X-basis projectors
    plus = np.outer(pauli_x_plus, pauli_x_plus.T)
    minus = np.outer(pauli_x_minus, pauli_x_minus.T)
  elif input == 1:
    
    # Eigenstates of Pauli Y observable
    pauli_y_plus = np.array([1, 1j])/np.sqrt(2)
    pauli_y_minus = np.array([1, -1j])/np.sqrt(2)
    
    # Y-basis projectors
    plus = np.outer(pauli_y_plus, pauli_y_plus.T)
    minus = np.outer(pauli_y_minus, pauli_y_minus.T)

  # Define measurement operators for the correct qubit
  if size == 0:
    M_plus = plus
    M_minus = minus
  else:
    M_plus = np.kron(plus, np.eye(size))
    M_minus = np.kron(minus, np.eye(size))

  # Compute probabilities
  P_plus = np.trace(M_plus @ rho @ M_plus.conj().T).real
  P_minus = np.trace(M_minus @ rho @ M_minus.conj().T).real

  # Choose measurement result with respect to the probabilities
  meas = np.random.choice(["plus", "minus"], p=[P_plus, P_minus])

  # Update the density matrix
  if meas == "plus":
    rho_updated = (M_plus @ rho @ M_plus.conj().T) / P_plus if P_plus > 0 else np.zeros_like(rho)
    result = 0
  elif meas == "minus":
    rho_updated = (M_minus @ rho @ M_minus.conj().T) / P_minus if P_minus > 0 else np.zeros_like(rho)
    result = 1

  # Trace out the measured qubit
  rho = partial_trace(rho_updated, [0])
  return rho, result