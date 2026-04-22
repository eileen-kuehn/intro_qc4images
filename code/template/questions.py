import ipywidgets as widgets
from IPython.display import display
import template.output as output
import template.widget_state_storage as storage
from template.settings import widget_language as wl
import html

translations = {
    "de": {
        "default_input_prompt": "Die Frage:",
        "default_input_description": "Die Antwort:",
        "default_success_message": "Die Antwort ist korrekt!",
        "default_error_message": "Deine Antwort ist noch nicht korrekt.",
        "placeholder": (
            "Gib hier die Antwort ein und bestätige anschließend die Eingabe."
        ),
        "save_button": "Speichern",
        "edit_button": "Bearbeiten",
        "check_button": "Prüfen",
        "answer_not_found": "Die Antwort wurde nicht gefunden.",
    },
    "en": {
        "default_input_prompt": "The question:",
        "default_input_description": "The answer:",
        "default_success_message": "The answer is correct!",
        "default_error_message": "Your answer is not correct yet.",
        "placeholder": "Enter your answer here and confirm the input.",
        "save_button": "Save",
        "edit_button": "Edit",
        "check_button": "Check",
        "answer_not_found": "The answer was not found.",
    },
}


WIDGET_TYPE = "Freitext"


def load_answer(identifier):
    state = storage.load_state(WIDGET_TYPE, identifier, None)
    if state is None:
        return None

    return state["Antwort"]


def store_answer(identifier, input_description, answer):
    state = {"Beschreibung": input_description, "Antwort": answer}
    storage.store_state(WIDGET_TYPE, identifier, state)


def prompt_answer(
    exercise_identifier,
    input_prompt=translations[wl]["default_input_prompt"],
    input_description=translations[wl]["default_input_description"],
):
    existing_answer = load_answer(exercise_identifier)

    # Define widgets
    output = widgets.Output()

    input_area = widgets.Textarea(
        placeholder=translations[wl]["placeholder"],
        description=f"{input_prompt}:",
        disabled=existing_answer is not None,
        value=existing_answer,
        rows=2,
        style=dict(description_width="initial"),
        layout=widgets.Layout(width="75%"),
    )

    def to_save_button(button):
        button.description = translations[wl]["save_button"]
        button.icon = "save"

    def to_edit_button(button):
        button.description = translations[wl]["edit_button"]
        button.icon = "edit"

    button = widgets.Button()

    if existing_answer is None:
        to_save_button(button)
    else:
        to_edit_button(button)

        with output:
            output.clear_output()
            _beautify_output(input_description, input_area.value)

    # Handle click logic
    def handle_click(button):
        if button.description == translations[wl]["save_button"]:
            input_area.disabled = True
            to_edit_button(button)

            with output:
                output.clear_output()

                _beautify_output(input_description, input_area.value)

            store_answer(exercise_identifier, input_description, input_area.value)
        else:
            input_area.disabled = False
            to_save_button(button)

    button.on_click(handle_click)

    # Show widget
    widget = widgets.HBox([input_area, button])
    display(widget)
    display(output)


def contains_check(solutions, equals_ignore_case=True, every_solution_present=False):
    def check(text):
        if every_solution_present:
            for solution in solutions:
                if equals_ignore_case and solution.lower() not in text.lower():
                    return False
                if not equals_ignore_case and solution not in text:
                    return False

            return True

        for solution in solutions:
            if equals_ignore_case and solution.lower() in text.lower():
                return True
            if not equals_ignore_case and solution in text:
                return True

        return False

    return check


def prompt_answer_with_check(
    exercise_identifier,
    input_prompt=translations[wl]["default_input_prompt"],
    input_description=translations[wl]["default_input_description"],
    check_func=None,
    success_message=translations[wl]["default_success_message"],
    error_message=translations[wl]["default_error_message"],
):
    existing_answer = load_answer(exercise_identifier)

    # Define widgets
    text_output = widgets.Output()
    check_output = widgets.Output()

    input_area = widgets.Textarea(
        placeholder=translations[wl]["placeholder"],
        description=f"{input_prompt}:",
        disabled=existing_answer is not None,
        value=existing_answer,
        rows=2,
        style=dict(description_width="initial"),
        layout=widgets.Layout(width="75%"),
    )

    def to_save_button(button):
        button.description = translations[wl]["save_button"]
        button.icon = "save"

    def to_edit_button(button):
        button.description = translations[wl]["edit_button"]
        button.icon = "edit"

    button = widgets.Button()

    if existing_answer is None:
        to_save_button(button)
    else:
        to_edit_button(button)

        with text_output:
            text_output.clear_output()
            _beautify_output(input_description, input_area.value)

    check_button = widgets.Button(
        description=translations[wl]["check_button"], icon="check-circle"
    )

    # Handle click logic
    def handle_click(button):
        check_output.clear_output()

        if button.description == translations[wl]["save_button"]:
            input_area.disabled = True
            to_edit_button(button)

            text_output.clear_output()
            with text_output:
                _beautify_output(input_description, input_area.value)

            store_answer(exercise_identifier, input_description, input_area.value)
        else:
            input_area.disabled = False
            to_save_button(button)

    button.on_click(handle_click)

    def handle_check_click(button):
        check_output.clear_output()

        with check_output:
            if check_func(input_area.value):
                output.correct(success_message)
            else:
                output.wrong(error_message)

    check_button.on_click(handle_check_click)

    # Show widget
    widget = widgets.HBox([input_area, widgets.VBox([button, check_button])])
    display(widget)
    display(text_output)
    display(check_output)


def _beautify_output(label, answer):
    html_source = """
    <div id="student-answer" class="alert alert-info">
      <h4>{label}</h4>
      {answer}
    </div>
    """.format(
        label=label, answer=html.escape(answer).replace("\n", "<br>")
    )

    output.html(html_source)


def print_answer(identifier):
    state = storage.load_state(WIDGET_TYPE, identifier, None)
    if state is None:
        print(translations[wl]["answer_not_found"])
        return

    _beautify_output(state["Beschreibung"], state["Antwort"])
