from IPython.display import HTML, display
from template.settings import widget_language as wl

translations = {
    "de": {
        "success": "Diese Antwort ist richtig!",
        "error": "Diese Antwort ist noch nicht richtig.",
    },
    "en": {
        "success": "This answer is correct!",
        "error": "This answer is not correct yet.",
    },
}


def correct(message=translations[wl]["success"]):
    display(
        HTML(
            f"""<div class="alert alert-success"> <i class="fas fa-check"></i> {message}</p></div>"""
        )
    )


def wrong(message=translations[wl]["error"]):
    display(
        HTML(
            f"""<div class="alert alert-danger"> <i class="fas fa-times"></i> {message}</p></div>"""
        )
    )


def html(html_source):
    display(HTML(html_source))
