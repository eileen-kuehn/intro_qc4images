import ipywidgets as widgets
from IPython.display import display
import template.output as output


def show_correct_text_selection(options):
    radio_buttons = []
    output_widget = widgets.Output()

    # Change manually all radio buttons on new selection.
    # Print the corresponding output.
    def on_change(properties):
        if properties["new"] is None:
            return

        clicked = properties["owner"]
        for button in radio_buttons:
            if button.options != clicked.options:
                button.value = None

    # Create all radio buttons
    for i in range(len(options)):
        unique_identifier = " " * i
        single_button = widgets.RadioButtons(
            options=[unique_identifier], value=None, layout=widgets.Layout(width="18px")
        )
        single_button.observe(on_change, names="value")

        radio_buttons.append(single_button)

    # Build the rows containing the radio button and the math widget
    rows = []
    for i, (text, correct, output_message) in enumerate(options):
        math_widget = widgets.HTMLMath(
            text, style=dict(font_size="15px"), layout=widgets.Layout(height="40px")
        )

        rows.append(widgets.HBox([radio_buttons[i], math_widget]))

    # Create check button
    check_button = widgets.Button(description="Überprüfen")

    def check_answer(ignored):
        with output_widget:
            output_widget.clear_output()

            selected_index = -1
            for i, radio_button in enumerate(radio_buttons):
                if radio_button.index is not None:
                    selected_index = i

            option = options[selected_index]
            if option[1]:
                output.correct(option[2])
            else:
                output.wrong(option[2])

    check_button.on_click(check_answer)

    rows.append(check_button)

    # Select first radio button
    radio_buttons[0].index = 0

    # Display the rows and output
    display(widgets.VBox(rows), output_widget)
