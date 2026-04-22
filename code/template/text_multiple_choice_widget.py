import ipywidgets as widgets
from IPython.display import display
import template.output as output
from template.settings import widget_language as wl

translations = {
    "de": {
        "check_button": "Antwort prüfen",
        "success": "Korrekt!",
        "missing": "Du hast noch richtige Antworten nicht ausgewählt.",
        "wrong": "Du hast falsche Antworten ausgewählt.",
        "nothing_selected": "Bitte wähle mindestens eine Option aus.",
    },
    "en": {
        "check_button": "Check answer",
        "success": "Correct!",
        "missing": "You missed one or more correct answers.",
        "wrong": "You selected one or more incorrect answers.",
        "nothing_selected": "Please select at least one option.",
    },
}


def show_multiple_choice_with_feedback(options, feedback_messages=None, height="35px"):
    checkboxes = []
    output_widget = widgets.Output()

    # Zeilen mit Checkboxen und Texten
    rows = []
    for i, (text, correct) in enumerate(options):
        checkbox = widgets.Checkbox(
            value=False, indent=False, layout=widgets.Layout(width="30px")
        )
        math_widget = widgets.HTMLMath(
            value=text,
            style=dict(font_size="20px"),
            layout=widgets.Layout(height=height),
        )
        row = widgets.HBox(
            [checkbox, math_widget], layout=widgets.Layout(align_items="center")
        )
        checkboxes.append((checkbox, correct))
        rows.append(row)

    # VBox für alle Auswahlzeilen
    options_box = widgets.VBox(rows)

    # Button rechts neben die Optionen
    check_button = widgets.Button(
        description=translations[wl]["check_button"],
        icon="check-circle",
        layout=widgets.Layout(margin="0 0 0 20px", height="fit-content"),
    )

    # Button-Klickfunktion
    def on_check_clicked(b):
        if feedback_messages is None:
            with output_widget:
                output_widget.clear_output()

                selected = [cb.value for cb, _ in checkboxes]
                if not any(selected):
                    output.wrong(translations[wl]["nothing_selected"])
                    return

                wrong_selected = any(
                    cb.value and not correct for cb, correct in checkboxes
                )
                missing_correct = any(
                    not cb.value and correct for cb, correct in checkboxes
                )

                if not wrong_selected and not missing_correct:
                    output.correct(translations[wl]["success"])
                elif wrong_selected:
                    output.wrong(translations[wl]["wrong"])
                else:
                    output.wrong(translations[wl]["missing"])
        else:
            with output_widget:
                output_widget.clear_output()

                selected = [cb.value for cb, _ in checkboxes]
                if not any(selected):
                    output.wrong(feedback_messages["nothing_selected"])
                    return

                wrong_selected = any(
                    cb.value and not correct for cb, correct in checkboxes
                )
                missing_correct = any(
                    not cb.value and correct for cb, correct in checkboxes
                )

                if not wrong_selected and not missing_correct:
                    output.correct(feedback_messages["success"])
                elif wrong_selected:
                    output.wrong(feedback_messages["wrong"])
                else:
                    output.wrong(feedback_messages["missing"])

    check_button.on_click(on_check_clicked)

    # Layout: Optionen und Button nebeneinander
    main_layout = widgets.HBox(
        [options_box, check_button], layout=widgets.Layout(align_items="flex-start")
    )

    display(main_layout, output_widget)
