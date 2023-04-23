import matplotlib.image as mpimg
from matplotlib.pyplot import imshow
from qiskit import QuantumCircuit, transpile, IBMQ
from qiskit_aer import AerSimulator
import numpy as np
from copy import copy

from ibmq_access import token, hub, group, project


def load_image(path):
    org_image = mpimg.imread(path)
    if np.max(org_image) <= 1:
        org_image *= 255
        org_image = org_image.astype(np.uint8)
    return copy(org_image)


"""
Here we can reduce the number of possible values for the image. If you call the function with `r_value = 2**x`, it guarantees that if you convert your pixel values to binary the last x bits will be zero. This hardly affects the image quality but reduces the number of qubits and hugely decreases the computational complexity of the mapping. Should also make the quantum image smoother. 

"""
def reduce_rgb_values(image, r_value):
    image = copy(image)
    height, width, channel = image.shape
    for h in range(height):
        for w in range(width):
            for c in range(channel):
                value = image[h, w, c]
                difference = value % r_value
                if difference < r_value/2:
                    value -= difference
                else:
                    value += (r_value - difference)
                if value > 255:
                    value -= r_value
                image[h, w, c] = value
                
    return image


def filling_zeros(binary, n):
    difference = (n - len(binary))*"0"
    return difference + binary

def get_result(circuit, backend=None, shots=1024, prob=True):
    if backend is None:
        backend = AerSimulator()
    elif type(backend) == str:
        try:
            provider = IBMQ.enable_account(
                token=token,
                hub=hub,
                group=group,
                project=project,
            )
        except IBMQ.IBMQAccountError: # we will run into that when trying to connect to already enabled account
            pass
        backend = provider.get_backend(backend)

    job_sim = backend.run(transpile(circuit, backend), shots=shots)
    result_sim = job_sim.result().get_counts()

    if prob:
        return {k:int(100*v/shots) for k, v in result_sim.items()}
    else:
        return result_sim

def create_mapping(noisy_circuit, backend=None, shots=1024):
    mapping = {}
    qubits = len(noisy_circuit.qubits)

    for i in range(2**qubits):
        encoding_circuit = QuantumCircuit(qubits)
        binary_number = bin(i)[2:]
        for index, q in enumerate(binary_number[::-1]): #LSB = Qubit 0
            if q == "1":
                encoding_circuit.x(index)
        encoding_circuit.barrier()

        full_circuit = encoding_circuit.compose(noisy_circuit)
        full_circuit.measure_all()
        
        counts = get_result(full_circuit, backend, shots, prob=False)
        mapping[filling_zeros(binary_number, qubits)] = max(counts, key=counts.get)

    print("Mapping:", mapping)
    return mapping

def create_rgb_mapping(noisy_circuit, backend=None, shots=1024, channels=3):
    qubits = len(noisy_circuit.qubits)

    rgb_mapping = {}

    for i in range(2**qubits):
        encoding_circuit = QuantumCircuit(qubits)
        for c in range(channels):
            
            binary_number = bin(i)[2:]
            for index, q in enumerate(binary_number[::-1]): #LSB = Qubit 0
                if q == "1":
                    encoding_circuit.x(index)
            encoding_circuit.barrier()

        full_circuit = encoding_circuit.compose(noisy_circuit)
        full_circuit.measure_all()
        
        counts = get_result(full_circuit, backend, shots, prob=False)

        rgb_mapping[filling_zeros(binary_number, qubits)] = max(counts, key=counts.get)

    print("Mapping:", rgb_mapping)
    return rgb_mapping

def convert_image(qubits, image, mapping, pixels_to_transform):
    image = copy(image)
    channels = image.shape[2]
    
    for pixel in pixels_to_transform:
        row = pixel[0]
        column = pixel[1]
        
        for channel in range(channels):        
            value = image[row, column, channel]
            b_value = bin(value)[2:]
            b_value2 = filling_zeros(b_value, 8)

            cut_b_value = b_value2[:qubits]

            new_b_value = mapping[cut_b_value] + (8-(qubits))*"0"

            image[row, column, channel] = int(new_b_value, 2)
                
    return image

def convert_rgb_image(qubits, image, mapping, pixels_to_transform):
    image = copy(image)
    channels = image.shape[2]
    
    for pixel in pixels_to_transform:
        row = pixel[0]
        column = pixel[1]
        
        cut_b_value = ""
        for channel in range(channels):        
            value = image[row, column, channel]
            b_value = bin(value)[2:]
            b_value2 = filling_zeros(b_value, 8)

            cut_b_value += b_value2[:qubits]

        new_b_value = mapping[cut_b_value]

        for channel in range(channels):        

            image[row, column, channel] = int(new_b_value[channel*qubits:(channel+1)*qubits] + (8-(qubits))*"0", 2)
                
    return image


def show_bw_image(image):
    imshow(image, cmap='gray', vmin=0, vmax=255)
