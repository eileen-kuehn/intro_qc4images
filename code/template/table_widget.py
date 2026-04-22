import ipywidgets as widgets
import pandas as pd
import numpy as np
from IPython.display import display
import template.widget_state_storage as storage
from template.settings import widget_language as wl
import template.output as output
from fractions import Fraction

WIDGET_TYPE = "Tabelle"

CORRECT = "Correct"
WRONG = "Wrong"

translations = {
    "de": {
        "save_button": "Speichern",
        "check_button": "Prüfen",
        "save_success": "Die Tabelle wurde gespeichert.",
        "correct": "Klasse! Die Tabelle ist korrekt.",
        "wrong": "Die Tabelle ist noch nicht korrekt ausgefüllt...",
    },
    "en": {
        "save_button": "Save",
        "check_button": "Check",
        "save_success": "The table has been saved.",
        "correct": "Great! The table is correct.",
        "wrong": "The table is not yet filled in correctly...",
    },
}


class Header:

    def __init__(self, text):
        self.text = text

    def to_widget(self, width):
        html = f"<div style='background-color: lightgray; text-align: center'><b>{self.text}</b></div>"
        return widgets.HTML(
            html,
            layout=widgets.Layout(border="1px solid", margin="0", width=f"{width}px"),
        )


class TextInput:

    def __init__(self, placeholder=""):
        self.placeholder = placeholder

    def to_widget(self, width):
        return widgets.Text(
            placeholder=self.placeholder,
            layout=widgets.Layout(border="1px solid", width=f"{width}px", margin="0"),
        )


class Content:
    def __init__(self, text):
        self.text = text

    def to_widget(self, width):
        html = f"<div style='text-align: center'><b>{self.text}</b></div>"
        return widgets.HTML(
            html,
            layout=widgets.Layout(border="1px solid", margin="0", width=f"{width}px"),
        )


def dataframe_to_table_widget(df: pd.DataFrame, fill_values: bool = True):
    """
    Konvertiert einen Pandas DataFrame in das Tabellen-Widget-Format.

    Parameter:
    - df: DataFrame mit Index und Spalten, optional auch mit Werten.
    - fill_values: Wenn True, werden die Zellwerte als Initialwerte in den TextInput-Feldern gesetzt.

    Rückgabe:
    - table_content: Liste von Listen, für show_table
    - column_widths: Einheitliche Spaltenbreite
    """
    table_content = []

    # Erste Zeile: Leere Ecke + Spaltenüberschriften
    header_row = [Header("")] + [Header(str(col)) for col in df.columns]
    table_content.append(header_row)

    # Zeilen: Header + TextInput (mit oder ohne Value)
    for index_label in df.index:
        row = [Header(str(index_label))]

        for col in df.columns:
            value = df.loc[index_label, col]
            if fill_values and pd.notna(value):
                row.append(TextInput(str(value)))
            else:
                row.append(TextInput(str(0)))

        table_content.append(row)

    # Einheitliche Spaltenbreite (optional)
    column_widths = [100] * (len(df.columns) + 1)

    return table_content, column_widths


def check_table(table_cells, correct_df):
    """
    Überprüft die Einträge einer Tabellen-Widget-Zelle (DataFrame-artig)
    gegen das DataFrame 'correct_df', unterstützt auch Brüche wie '1/2'.
    """
    try:
        # Entferne Header-Zeile und -Spalte
        data_only = [row[1:] for row in table_cells[1:]]

        # Konvertiere Zellinhalte in float, unterstütze Brüche wie "1/3"
        def parse_value(cell):
            try:
                return float(Fraction(str(cell).strip()))
            except (ValueError, ZeroDivisionError):
                return 0.0

        user_matrix = [[parse_value(cell) for cell in row] for row in data_only]

        user_df = pd.DataFrame(
            user_matrix, columns=correct_df.columns, index=correct_df.index
        )

        # Vergleich mit korrekt gelöster Matrix
        if np.allclose(user_df.values, correct_df.values, atol=1e-2):
            return CORRECT, translations[wl]["correct"]
        else:
            return WRONG, translations[wl]["wrong"]

    except Exception as e:
        return WRONG, f"Fehler beim Prüfen der Tabelle: {e}"


def show_table(
    exercise_identifier, table_content, column_widths, correct_df=None, check_func=None
):
    output_widget = widgets.Output()
    entries = _load_table_entries(exercise_identifier)
    all_widgets = [
        ["" for _ in range(len(table_content[0]))] for _ in range(len(table_content))
    ]

    # Create rows
    rows = []
    text_inputs = []

    for j, row in enumerate(table_content):
        row_widgets = []

        for i, elem in enumerate(row):
            width = column_widths[i]
            widget = elem.to_widget(width)

            row_widgets.append(widget)
            all_widgets[j][i] = widget

            if isinstance(elem, TextInput):
                if entries is not None:
                    entry = entries[len(text_inputs)]
                    widget.value = entry

                text_inputs.append(widget)

        rows.append(widgets.HBox(row_widgets))

    # Create buttons
    save_button = widgets.Button(
        description=translations[wl]["save_button"],
        icon="save",
        layout=widgets.Layout(margin="0" if check_func is None else "5"),
    )
    check_button = widgets.Button(
        description=translations[wl]["check_button"],
        icon="check-circle",
        layout=widgets.Layout(margin="5"),
    )

    def on_save(ignored):
        entries = list(map(lambda w: w.value, text_inputs))
        _store_table_entries(exercise_identifier, entries)

        with output_widget:
            output_widget.clear_output()
            output.correct(translations[wl]["save_success"])

    def on_check(ignored):
        text_values = [
            ["" for _ in range(len(table_content[0]))]
            for _ in range(len(table_content))
        ]

        for j in range(len(text_values)):
            for i in range(len(text_values[0])):
                text_values[j][i] = all_widgets[j][i].value
        if correct_df is None:
            result, message = check_func(text_values)
        else:
            result, message = check_func(text_values, correct_df)

        with output_widget:
            output_widget.clear_output()

            if result == CORRECT:
                output.correct(message)
            else:
                output.wrong(message)

    save_button.on_click(on_save)
    check_button.on_click(on_check)

    # Display table
    if check_func is None:
        rows[-1].children += (save_button,)
        display(widgets.VBox(rows), output_widget)
    else:
        display(
            widgets.HBox(
                [widgets.VBox(rows), widgets.VBox([save_button, check_button])]
            ),
            output_widget,
        )


def show_tabel_from_df(exercise_identifier, to_fill_df, correct_df):
    if not (
        to_fill_df.index.equals(correct_df.index)
        and to_fill_df.columns.equals(correct_df.columns)
        and to_fill_df.shape == correct_df.shape
    ):
        output.wrong(
            "Die auszufüllende Tabelle und der musterlösungs Tabelle haben nicht den selben Aufbau, überprüfe nochmal die Spalten und Zeilenbenennung."
        )
        return
    table_content, column_widths = dataframe_to_table_widget(to_fill_df, True)
    show_table(
        "AB5-3m", table_content, column_widths, correct_df, check_func=check_table
    )


def _store_table_entries(identifier, entries):
    state = {"Einträge": entries}
    storage.store_state(WIDGET_TYPE, identifier, state)


def _load_table_entries(identifier):
    state = storage.load_state(WIDGET_TYPE, identifier)
    if state is None:
        return None

    return state["Einträge"]
