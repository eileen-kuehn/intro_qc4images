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
quantum_cat_mapping = widgets.Output()


def reduce_values(qubits):
    global image
    image = reduce_rgb_values(original_image, qubits)
    plt.imshow(image)
    plt.show()
    return


qubit_cat = interactive(reduce_values, qubits=qubits)


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

left_x = rect.children[0]
left_y = rect.children[1]
bottom_x = rect.children[2]
bottom_y = rect.children[3]
left_box = widgets.HBox([left_x, left_y])
bottom_box = widgets.HBox([bottom_x, bottom_y])
cat_selection = widgets.VBox([left_box, bottom_box, rect.children[4]])


def process_image(option):
    global quantum_circuit
    current_circuit = None
    description = """
Diese Katze wurde nicht durch einen Quantencomputer bearbeitet. Schau dir ruhig
auch den Quantenschaltkreis an, dieser sollte leer sein. Es wird also keine
Operation, also kein Gate, auf unseren Qubits ausgeführt.
"""
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
        description = """
Wir können Verschränkungen nutzen, um den Zustand zweier Qubits zu tauschen und
somit auch die Farben in unserem Bild. Dazu erzeugen wir einen Quantenschaltkreis
mit 3 mal so vielen Qubits wie wir bisher gebraucht haben, da wir nun alle 3 
Farbkanäle abbilden wollen.
Anschließend tauschen wir jeweils jedes dritte Qubits miteinander.
"""
    elif option == "Verrauschte Katze":
        # quantum_circuit = QuantumCircuit(qubits.value * 3)
        REPS = 7  # how often do you want to repeat your circuit ?
        overall_quantum_circuit = QuantumCircuit(3 * qubits.value)
        for i in range(REPS):
            if len(quantum_circuit.qubits) < len(overall_quantum_circuit.qubits):
                for i in range(3):
                    base = len(quantum_circuit.qubits) * i
                    overall_quantum_circuit.compose(quantum_circuit, inplace=True, qubits=range(base, base + len(quantum_circuit.qubits)))
                overall_quantum_circuit.barrier()
                for i in range(3):
                    base = len(quantum_circuit.qubits) * i
                    overall_quantum_circuit.compose(quantum_circuit.inverse(), inplace=True, qubits=range(base, base + len(quantum_circuit.qubits)))
                overall_quantum_circuit.barrier()
            else:
                overall_quantum_circuit.compose(quantum_circuit, inplace=True)
                overall_quantum_circuit.barrier()
                overall_quantum_circuit.compose(quantum_circuit.inverse(), inplace=True)
                overall_quantum_circuit.barrier()
        backend = FakeMelbourne()
        mapping = create_rgb_mapping(overall_quantum_circuit, backend=backend)
        q_image = convert_rgb_image(qubits.value, image, mapping, pixels_to_transform)
        current_circuit = overall_quantum_circuit
        description = """
Bisher liefen die erzeugten Katenzbilder und Berechnung in einer "idealen" Welt.
Das heißt, wir hatten keine Störeinflüsse von außen und die Simulationen lieferten
stets das Ergebnis, das wir mathematisch auch erwarten würden.
Nun sind Quantencomputer heutzutage leider noch alles andere als perfekt. 
Um uns das mal genauer anzuschauen, zeigen wir dir hier noch eine weitere tolle
Eigenschaft von Quantencomputern. Jede Operation, die wir auf einem solchen
Gerät ausführen ist (bis auf die Messung am Ende) umkehrbar!
Das bedeutet, wir können jeden Schaltkreis einfach nehmen, umdrehen und an
das Original anhängen.
Das Ergebnis sollte im Idealfall ein Schaltkreis sein, der nichts an unserem
Bild ändert... oder?
<br/><br/>
Huch! Wie du siehst, ist da wohl was schiefgegangen, oder?
Nein, leider nicht. Die heutigen Quantencomputer sind in der Tat sehr 
fehleranfällig.
<br/><br/>
Aber Zeiten ändern sich! Die Leute von IBM, deren Maschinen wir gerade verwenden
und viele anderen Forschenden auf der Welt, versuchen Quantencomputer so schnell
wie möglich fehlerfrei und vor allem auch größer zu bauen. Dann können wir unsere
Katzenbilder bald schon in voller Größe und Pixeldichte darstellen.
"""
    elif option == "Zufällige Katze":
        quantum_circuit = QuantumCircuit(qubits.value)
        for i in range(qubits.value):
            quantum_circuit.h(i)
        mapping = create_mapping(quantum_circuit)
        q_image = convert_image(qubits.value, image, mapping, pixels_to_transform)
        current_circuit = quantum_circuit
        description = """
Wie du beim Anschauen der invertierten Katze lernen konntest, können wir auf dem 
Nordpol unseres Qubits den Wert 0 abbilden und auf Südpol den Wert 1. Beim Messen
des Qubits bekommen wir in dieser Ebene dann entweder den Wert 0 oder den Wert 1.
Was meinst du, was passiert, wenn wir den Zustand des Qubits so ändern, dass sich
dieser genau zwischen 0 und 1, also genau auf dem Äquator, befindet?

<img src="images/plusstate.png" alt="Plus Status" />
<br/>
Auf dem Äquator messen wir mit einer Wahrscheinlichkeit von 50% 0 oder 1.
Erst durch die Messung selbst wird festgelegt, welchen Zustand das Qubit hat.
Ein Gate, mit dem wir den Zustand so ändern können, ist das sogenannte 
<i>Hadamard Gate</i>. Schau dir gleich mal den Quantenschaltkreis an, um zu
schauen, wie genau wir diesen verändert haben, um die einzelnen Pixel unserer
Katze zufällig zu verändern.
<br/><br/>
Klasse! Jetzt weißt du ja schon, dass so ein Qubit mehr Zustände annehmen kann,
als ein klassissches Bit. Es gibt aber noch mehr! Bisher war immer die Rede von
einem einzigen Qubit. Wir können im Quantencomputing aber auch zwei Qubits
miteinander verschränken, so, dass wenn wir eins der beiden messen, das andere
exakt den gleichen Zustand annehmen wird.
Das ist ein bisschen schwierig zu erklären, am Besten fragst du uns einfach
wenn du mehr dazu wissen möchtest!
"""
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
transformed_quantum_cat = quantum_cat.children[1]
transformed_quantum_cat.layout.width = "315px"
transformed_quantum_cat.layout.max_width = "315px"
transformed_quantum_cat.layout.min_width = "315px"

details = widgets.HBox([
    quantum_cat.children[1], 
    widgets.Accordion(children=[quantum_cat_description, quantum_cat_circuit, quantum_cat_mapping], titles=["Beschreibung", "Quantenschaltkreis", "Mapping"])])
cat_types = widgets.VBox([quantum_cat.children[0], details])
