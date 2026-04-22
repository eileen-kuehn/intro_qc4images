import numpy as np
from template import questions
from template.widget_state_storage import load_state
import utils
from utils import imshow, load_image
from template import output
import template.table_widget as table
from copy import copy


def setup_erfolg():
    output.correct("Pakete, Daten und Funktionen erfolgreich geladen.")


def show_bw_image(identifier):
    data = load_state("Tabelle", identifier)["Einträge"]
    for elem in data:
        if not elem.isnumeric():
            output.wrong("Alle Werte müssen ganze Zahlen zwischen 0 und 255 sein.")
            return
    return utils.show_bw_image(np.array(data, dtype=np.uint8).reshape((4, 3)))


def check_1a():
    data = load_state("Tabelle", "AB2-1a")["Einträge"]
    for elem in data:
        if not elem.isnumeric():
            output.wrong("Alle Werte müssen ganze Zahlen zwischen 0 und 255 sein.")
            return
        cell_value = int(elem)
        if cell_value < 0 or cell_value > 255:
            output.wrong("Alle Werte müssen zwischen 0 und 255 liegen.")
            return
    all_white = True
    for elem in data:
        if int(elem) != 0:
            all_white = False
            break
    if all_white:
        output.wrong(
            "Alle Werte sind zwar korrekt, aber dein Bild ist komplett schwarz. Probiere doch mal andere Werte >0 und schau, wie sich dein Bild verändert."
        )
        return
    output.correct("Alle Werte sind korrekt. Tolles Bild!")


def check_2b(count):
    if count is None:
        output.wrong("Gib eine Zahl ein.")
    elif not isinstance(count, int) or count < 0:
        output.wrong("Die Zahl muss eine positive ganze Zahl sein.")
    elif count == 165060:
        output.correct("Das ist die richtige Anzahl an Werten für die kleine Katze!")
    else:
        output.wrong("Das ist nicht die richtige Anzahl.!")


def check_2c(pixel):
    if pixel == 239:
        output.correct("Das ist der richtige Wert für den Rot-Kanal dieses Pixels!")
    elif pixel == 213:
        output.wrong(
            "Der Wert ist leider falsch. Hast du bedacht, dass wir in der Informatik von 0 zu zählen beginnen?"
        )
    else:
        output.wrong("Das ist nicht der richtige Wert für den Rot-Kanal dieses Pixels!")


def show_image_table(identifier):
    table_content = [
        [table.TextInput(), table.TextInput(), table.TextInput()],
        [table.TextInput(), table.TextInput(), table.TextInput()],
        [table.TextInput(), table.TextInput(), table.TextInput()],
        [table.TextInput(), table.TextInput(), table.TextInput()],
    ]
    column_widths = [100, 100, 100]

    def check_table(text_cells):
        for row in text_cells:
            for cell in row:
                if not cell.isnumeric():
                    return (
                        table.WRONG,
                        "Alle Werte müssen ganze Zahlen zwischen 0 und 255 sein.",
                    )
                cell_value = int(cell)
                if cell_value < 0 or cell_value > 255:
                    return table.WRONG, "Alle Werte müssen zwischen 0 und 255 liegen."
        return (
            table.CORRECT,
            "Alle Werte sind korrekt. Vergiss nicht, zu speichern, damit du dein Bild anschauen kannst.",
        )

    table.show_table(identifier, table_content, column_widths, check_func=check_table)


def prompt_2a():
    questions.prompt_answer(
        "AB2-2a",
        input_prompt="Deine Hypothese",
        input_description="Deine Hypothese zur Dimension von Farbbildern:",
    )
