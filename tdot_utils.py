import ipywidgets as widgets
import matplotlib.pyplot as plt
from copy import copy
from utils import load_image, reduce_rgb_values, print_mapping, create_rgb_qubits
from ipywidgets import interact, interact_manual, interactive
from qiskit import QuantumCircuit
from qiskit import Aer
from qiskit.circuit.random import random_circuit
from qiskit.providers.fake_provider import FakeManilaV2, FakeBoeblingen, FakeMelbourne
from utils import (
    filling_zeros,
    create_mapping,
    convert_image,
    convert_rgb_image,
    get_result,
    create_rgb_mapping,
)
from IPython.core.display_functions import display


qubits = widgets.IntSlider(min=0, max=8, value=2, description="Qubit Anzahl")
cat_path = "./images/Cat.jpg"
original_image = load_image(cat_path)
image = original_image
pixels_to_transform = []
quantum_circuit = None
quantum_cat_circuit = widgets.Output()
quantum_cat_description = widgets.Output()
quantum_cat_description.layout.width = "350px"
quantum_cat_mapping = widgets.Output()


def reduce_values(qubits):
    global image
    image = reduce_rgb_values(original_image, qubits)
    plt.imshow(image)
    plt.show()
    return


def show_rectangular_selection(left_x, left_y, bottom_x, bottom_y):
    global pixels_to_transform
    # wir starten wieder mit einer leeren Liste
    pixels_to_transform = []

    # wir definieren das Rechteck
    for row in range(left_y, bottom_y):
        for column in range(left_x, bottom_x):
            pixel = [row, column]
            pixels_to_transform.append(pixel)

    image_copy = copy(image)

    for pixel in pixels_to_transform:
        row = pixel[0]
        column = pixel[1]

        image_copy[row, column, 0] = 255  # R
        image_copy[row, column, 1] = 255  # G
        image_copy[row, column, 2] = 255  # B

    plt.imshow(image_copy)
    plt.show()


rect = interactive(
    show_rectangular_selection,
    left_x=widgets.IntSlider(
        min=0, max=image.shape[0], value=200, description="Links (x)"
    ),
    left_y=widgets.IntSlider(
        min=0, max=image.shape[1], value=30, description="Links (y)"
    ),
    bottom_x=widgets.IntSlider(
        min=0, max=image.shape[0], value=500, description="Rechts (x)"
    ),
    bottom_y=widgets.IntSlider(
        min=0, max=image.shape[1], value=330, description="Rechts (y)"
    ),
)


def process_image(option):
    global quantum_circuit
    current_circuit = None
    description = "Diese Katze wurde nicht durch einen Quantencomputer bearbeitet. Schau dir ruhig auch den Quantenschaltkreis an, dieser sollte leer sein. Es wird also keine Operation, also kein Gate, auf unseren Qubits ausgeführt."
    if option == "Invertierte Katze":
        quantum_circuit = QuantumCircuit(qubits.value)
        for i in range(qubits.value):
            quantum_circuit.x(i)
        mapping = create_mapping(quantum_circuit)
        q_image = convert_image(qubits.value, image, mapping, pixels_to_transform)
        current_circuit = quantum_circuit
        description = """
Um eine Zahl zu invertieren, multipliziert man sie beispielsweise mit -1. Auf Quantencomputern benutzen wir dafür das sogenannte <i>X-Gate</i>. Das X-Gate sorgt dafür, dass der aktuelle Zustand unseres Qubits invertiert wird.
Es wird also quasi aus jeder 0 eine 1 gemacht. Das passt ja: auf deinem Circuit befinden sich auf jedem Qubit ein X-Gate, das den Wert ändert. 
<br/><br/>
Wahrscheinlich hast du es schon gemerkt, aber Qubits sind für einen Quantencomputer das, was Bits für unsere klassischen Computer sind; Die kleinste Informationseinheit die wir mit diesen Geräten abbilden können.
Das Spannende ist nun, mit so einem Qubit kann man viel mehr machen, als wir es mit einem klassischen Bit könnte!
<br/><br/>
Ein Qubit kann nicht nur entweder 0 oder 1 sein, sondern beides gleichzeitig mit einer gewissen Wahrscheinlichkeit. Klingt ein bisschen komisch?
<br/><br/>
Stell dir jetzt einfach vor, im klassischen haben wir nur einen Strich an dessen Endpunkten entweder `0` oder `1` steht. Genau diese und nur diese beide Zustände können wir einnehmen.
Im Quantencomputing haben wir nun für ein Qubit die Möglichkeit als Zustand jeden erdenklichen Punkt auf der Oberfläche einer Kugel einzunehmen. 
<img src="images/qbits.png" alt="Bit und Qubit Darstellung"/>
"""
    elif option == "Vertauschte Katze":
        rgb_qubits = create_rgb_qubits(qubits.value)
        quantum_circuit = QuantumCircuit(*rgb_qubits)
        quantum_circuit.swap(0, 3)
        quantum_circuit.swap(1, 4)
        quantum_circuit.swap(2, 5)
        mapping = create_rgb_mapping(quantum_circuit)
        q_image = convert_rgb_image(qubits.value, image, mapping, pixels_to_transform)
        current_circuit = quantum_circuit
    elif option == "Verrauschte Katze":
        # quantum_circuit = QuantumCircuit(qubits.value * 3)
        REPS = 7  # how often do you want to repeat your circuit ?
        overall_quantum_circuit = QuantumCircuit(3 * qubits.value)
        for i in range(REPS):
            overall_quantum_circuit.compose(quantum_circuit, inplace=True)
            overall_quantum_circuit.barrier()
            overall_quantum_circuit.compose(quantum_circuit.inverse(), inplace=True)
            overall_quantum_circuit.barrier()
        backend = FakeMelbourne()
        mapping = create_rgb_mapping(overall_quantum_circuit, backend=backend)
        q_image = convert_rgb_image(qubits.value, image, mapping, pixels_to_transform)
        current_circuit = overall_quantum_circuit
    elif option == "Zufällige Katze":
        quantum_circuit = QuantumCircuit(qubits.value)
        for i in range(qubits.value):
            quantum_circuit.h(i)
        mapping = create_mapping(quantum_circuit)
        q_image = convert_image(qubits.value, image, mapping, pixels_to_transform)
        current_circuit = quantum_circuit
    else:
        quantum_circuit = QuantumCircuit(qubits.value)
        mapping = create_mapping(quantum_circuit)
        q_image = convert_image(qubits.value, image, mapping, pixels_to_transform)
        current_circuit = quantum_circuit

    plt.imshow(q_image)
    plt.show()

    with quantum_cat_circuit:
        quantum_cat_circuit.clear_output()
        display(current_circuit.draw("mpl"))
    with quantum_cat_description:
        quantum_cat_description.clear_output()
        display(widgets.HTML(value=description))
    with quantum_cat_mapping:
        quantum_cat_mapping.clear_output()
        print_mapping(mapping)


quantum_cat = interactive(
    process_image,
    option=widgets.ToggleButtons(
        options=[
            "Originale Katze",
            "Invertierte Katze",
            "Zufällige Katze",
            "Vertauschte Katze",
            "Verrauschte Katze",
        ],
        description="Verarbeitung des Bildes mit dem Quantencomputer",
    ),
)
