from template import output, questions
import template.table_widget as table

multiply = None


def setup_erfolg():
    output.correct("Pakete, Daten und Funktionen erfolgreich geladen.")


def show_datatype_table():
    table_content = [
        [
            table.Header("Variablenzuweisung"),
            table.Header("Datentyp"),
        ],
        [table.Content("<code>var1 = 5 + 6.1</code>"), table.TextInput()],
        [table.Content("<code>var2 = True + 1</code>"), table.TextInput()],
        [table.Content("<code>var3 = '1' + 1</code>"), table.TextInput()],
    ]
    column_widths = [250, 100]

    # Optional
    def check_table(text_cells):
        correct = True
        outputstring = ""
        if str.lower(text_cells[1][1]) in ("float", "kommazahl", "gleitkommazahl"):
            outputstring += "Der Datentyp für <code>var1</code> ist korrekt."
            output.correct,
        else:
            correct = False
            outputstring += "Der Datentyp für <code>var1</code> ist leider falsch. Überlege, was die Summe aus einer Ganzzahl und einer Kommazahl ergibt."
        if str.lower(text_cells[2][1]) in ("int", "ganzzahl", "integer"):
            outputstring += "<br/>Der Datentyp für <code>var2</code> ist korrekt."
        else:
            correct = False
            outputstring += "<br/>Der Datentyp für <code>var2</code> ist leider falsch. Überlege, was die Summe aus einem Wahrheitswert und einer Ganzzahl ergibt."
        if str.lower(text_cells[3][1]) in ("fehler", "error", "typeerror"):
            outputstring += "<br/>Der Datentyp für <code>var3</code> ist korrekt."
        else:
            correct = False
            outputstring += "<br/>Der Datentyp für <code>var3</code> ist leider falsch."
        if correct:
            return table.CORRECT, outputstring
        else:
            return table.WRONG, outputstring

    table.show_table("AB1-2a", table_content, column_widths, check_func=check_table)


def prompt_1b():
    questions.prompt_answer(
        "AB1-2a",
        input_prompt="Deine Hypothese",
        input_description="Deine Hypothese zur Frage 1b:",
    )


def check_3a(fn):
    if fn is not None:
        for a, b in ((0, 0), (-1, 2), (3, 3), (-10, -2)):
            if a * b != fn(a, b):
                output.wrong(
                    f"Bitte überprüfe deine Implementierung, z.B. für {a} und {b}"
                )
                return
        else:
            output.correct("Deine Implementierung scheint korrekt. Super!")
    else:
        output.wrong(
            "Bitte erstelle noch deine Implementierung der Funktion `multiply`."
        )


def prompt_4a():
    check_func = questions.contains_check(
        ["Zeile 5", "Zeile 10", "Zeile 13", "Zeile 16", "Zeile 21"],
        equals_ignore_case=False,
        every_solution_present=True,
    )
    questions.prompt_answer_with_check(
        "AB1-4a",
        input_prompt="Deine Antwort",
        input_description="Deine Antwort für die if Abfragen:",
        check_func=check_func,
        success_message="Korrekt! Du hast die korrekten if Abfragen identifiziert.",
        error_message="Deine Antwort enthält noch nicht alle Zeilen, die ausgegeben werden.",
    )


def prompt_6a():
    questions.prompt_answer_with_check(
        "AB1-6a",
        input_prompt="Deine Antwort",
        input_description="Deine Antwort für die Ausgabe:",
        check_func=lambda value: value == "[1, 2, 3, 4, 5]",
        success_message="Korrekt! Genau das wird ausgegeben.",
        error_message="Das stimmt so nicht ganz. Denk nochmals darüber nach oder probier es gern selbst mal aus.",
    )
