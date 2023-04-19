import matplotlib.image as mpimg
from matplotlib.pyplot import imshow
from qiskit import QuantumCircuit, transpile
import numpy as np
from copy import copy

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


def create_mapping(qubits, backend, noisy_circuit, shots):
    mapping = {}

    for i in range(2**qubits):
        encoding_circuit = QuantumCircuit(qubits)
        binary_number = bin(i)[2:]
        for index, q in enumerate(binary_number[::-1]): #LSB = Qubit 0
            if q == "1":
                encoding_circuit.x(index)
        encoding_circuit.barrier()

        full_circuit = encoding_circuit.compose(noisy_circuit)
        full_circuit.measure_all()

        job_sim = backend.run(transpile(full_circuit, backend), shots=shots)
        result_sim = job_sim.result()
        counts = result_sim.get_counts(full_circuit)
        mapping[filling_zeros(binary_number, qubits)] = max(counts, key=counts.get)

    print("Mapping:", mapping)
    return mapping


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
            new_b_value = mapping[cut_b_value] + (8-qubits)*"0"

            image[row, column, channel] = int(new_b_value, 2)
                
    return image


def show_bw_image(image):
    imshow(image, cmap='gray', vmin=0, vmax=255)
