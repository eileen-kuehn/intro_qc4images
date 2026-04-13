import ipywidgets as widgets
from IPython.display import display
import template.output as output


def show_text_selection(options, height="35px"):
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

        with output_widget:
            output_widget.clear_output()
            option = options[len(clicked.options[0])]
            if option[1]:
                output.success(option[2])
            else:
                output.error(option[2])

    # Create all radio buttons
    for i in range(len(options)):
        unique_identifier = " " * i
        single_button = widgets.RadioButtons(
            options=[unique_identifier],
            value=None,
            layout=widgets.Layout(width="20px")
        )
        single_button.observe(on_change, names='value')

        radio_buttons.append(single_button)

    # Build the rows containing the radio button and the math widget
    rows = []
    for i, (text, correct, output_message) in enumerate(options):
        math_widget = widgets.HTMLMath(text, style=dict(font_size="20px"), layout=widgets.Layout(height=height))

        rows.append(widgets.HBox([radio_buttons[i], math_widget]))

    # Display the rows and output
    display(widgets.VBox(rows), output_widget)