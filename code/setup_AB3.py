from ipywidgets import widgets, interactive
from IPython.display import display
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

from qiskit import QuantumCircuit, QuantumRegister
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
    create_rgb_qubits,
    load_image,
    reduce_rgb_values,
    print_mapping,
)

from template import output, questions, widget_state_storage
from template.settings import widget_language as wl


def setup_erfolg():
    output.correct("Pakete, Daten und Funktionen erfolgreich geladen.")


def show_bit_prompt():
    def check_func(answer):
        if answer.strip().isnumeric() and int(answer.strip()) == 8:
            return True
        return False

    questions.prompt_answer_with_check(
        "AB3-1a",
        input_prompt="Wie viele Bits werden benötigt?",
        input_description="Anzahl Bits",
        check_func=check_func,
        success_message="Richtig! 8 Bits können 256 Werte darstellen, von 0 bis 255.",
        error_message="Das ist leider nicht korrekt. Überlege, wie viele Werte du mit einer bestimmten Anzahl von Bits darstellen kannst. Mit 1 Bit kannst du 2 Werte darstellen (0 und 1), mit 2 Bits kannst du 4 Werte darstellen (00, 01, 10, 11), und so weiter. Versuche es noch einmal!",
    )


image_path = "../images/Cat.jpg"
original_image = load_image(image_path)
image = original_image


def reduce_values(qubits):
    global image
    widget_state_storage.store_state(
        widget_type="IntSlider",
        identifier="AB3-1b",
        state={"Wert": qubits},
    )
    image = reduce_rgb_values(original_image, qubits)
    plt.imshow(image)
    plt.show()
    return


def show_qubit_slider():
    existing_answer = widget_state_storage.load_state(
        widget_type="IntSlider", identifier="AB3-1b", default_value={"Wert": 2}
    )

    # Define widgets
    slider = widgets.IntSlider(
        min=0, max=8, value=existing_answer["Wert"], description="Qubit Anzahl"
    )

    # Show widget
    display(interactive(reduce_values, qubits=slider))


def my_qubit_count():
    return widget_state_storage.load_state(
        widget_type="IntSlider", identifier="AB3-1b", default_value={"Wert": 2}
    )["Wert"]


def my_reduced_image():
    return reduce_rgb_values(image, my_qubit_count())


def my_pixels_to_transform():
    height, width = original_image.shape[:2]
    return [(i, j) for i in range(height) for j in range(width)]


def prompt_3b():
    questions.prompt_answer_with_check(
        exercise_identifier="AB3-3b",
        input_prompt="Wie hoch ist die Wahrscheinlichkeit, 0 zu messen?",
        check_func=lambda x: x.strip() == "50"
        or x.strip() == "50%"
        or x.strip() == "50 Prozent"
        or x.strip() == "0.5",
        success_message="Richtig! Da wir auf dem Äquator sind, ist die Wahrscheinlichkeit, 0 zu messen, 50%.",
        error_message="Das ist leider nicht korrekt. Überlege, dass der Zustand auf dem Äquator bedeutet, dass das Qubit mit gleichen Teilen in Superposition von 0 und 1 ist. Versuche es noch einmal!",
    )
