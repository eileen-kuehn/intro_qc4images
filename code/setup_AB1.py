from template import output
import template.table_widget as table


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
        if str.lower(text_cells[1][1]) in ("float", "komma"):
            outputstring += "Der Datentyp für <code>var1</code> ist korrekt."
            output.correct,
        else:
            correct = False
            outputstring += "Der Datentyp für <code>var1</code> ist leider falsch. Überlege, was die Summe aus einer Ganzzahl und einer Kommazahl ergibt."
        if str.lower(text_cells[2][1]) in ("int", "ganzzahl"):
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
