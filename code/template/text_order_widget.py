import ipywidgets as widgets
from IPython.display import display
import random
import template.output as output
from template.settings import widget_language as wl

translations = {
    "de": {
        "check_button": "Reihenfolge prüfen",
        "success": "Korrekt!",
        "error": "Die Reihenfolge ist noch nicht korrekt.",
    },
    "en": {
        "check_button": "Check order",
        "success": "Correct!",
        "error": "The order is not correct yet.",
    },
}


def show_text_order(options, option_width="75%"):
    text_widgets = []
    row_widgets = []

    output_widget = widgets.Output()

    # Randomize options
    def randomize():
        shuffled_options = options.copy()
        random.shuffle(shuffled_options)

        if shuffled_options == options:
            return randomize()
        else:
            return shuffled_options

    # Build rows (text, up, and down buttons)
    for i, option in enumerate(randomize()):
        text_widget = widgets.HTML(
            _format_option(option), layout=widgets.Layout(width=option_width)
        )
        up_button = widgets.Button(icon="chevron-up", disabled=i == 0)
        down_button = widgets.Button(
            icon="chevron-down", disabled=i == len(options) - 1
        )

        def up(idx, button):
            up_text = text_widgets[idx - 1].value
            curr_text = text_widgets[idx].value

            text_widgets[idx - 1].value = curr_text
            text_widgets[idx].value = up_text

        def down(idx, ignored):
            down_text = text_widgets[idx + 1].value
            curr_text = text_widgets[idx].value

            text_widgets[idx + 1].value = curr_text
            text_widgets[idx].value = down_text

        up_button.on_click(lambda b, i=i: up(i, b))
        down_button.on_click(lambda b, i=i: down(i, b))

        text_widgets.append(text_widget)
        row_widgets.append(widgets.HBox([text_widget, up_button, down_button]))

    # Check if order is correct
    def check_order(ignored):
        for i, option in enumerate(options):
            if text_widgets[i].value != _format_option(options[i]):
                with output_widget:
                    output_widget.clear_output()
                    output.wrong(translations[wl]["error"])
                return

        with output_widget:
            output_widget.clear_output()
            output.correct(translations[wl]["success"])

    # Build check button
    check_button = widgets.Button(
        description=translations[wl]["check_button"], icon="check-circle"
    )
    check_button.on_click(check_order)

    display(widgets.VBox(row_widgets))
    display(check_button)
    display(output_widget)


def _format_option(option):
    return f"<b>{option}</b>"
