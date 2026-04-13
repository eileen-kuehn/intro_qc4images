from ipywebrtc import CameraStream, AudioRecorder
import time
import os
import ipywidgets as widgets
from template.settings import widget_language as wl
from IPython.display import display

translations = {
    "de": {
        "start_recording": "Aufnahme starten",
        "save_and_play": "Aufnahme speichern und anhören",
    },
    "en": {
        "start_recording": "Start recording",
        "save_and_play": "Save and play recording",
    },
}


def show_audio_recorder(output_audio_file_path, duration=1):
    output = widgets.Output()
    camera = CameraStream(constraints={"audio": True, "video": False})
    recorder = AudioRecorder(stream=camera)

    def record_audio(ignored):
        start_btn.disabled = True

        recorder.recording = True
        time.sleep(duration)
        recorder.recording = False

        start_btn.disabled = True
        save_btn.disabled = False

    def save_and_play_audio(ignored):
        directory = os.path.dirname(output_audio_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        recorder.save(output_audio_file_path)
        with output:
            audio_player = widgets.Audio.from_file(
                output_audio_file_path, autoplay=False, loop=False, controls=True
            )
            display(audio_player)

    start_btn = widgets.Button(description=translations[wl]["start_recording"])
    save_btn = widgets.Button(
        description=translations[wl]["save_and_play"],
        disabled=True,
        layout=widgets.Layout(width="auto"),
    )
    start_btn.on_click(record_audio)
    save_btn.on_click(save_and_play_audio)

    buttons = widgets.HBox([start_btn, save_btn])
    display(widgets.VBox([buttons, output]))
