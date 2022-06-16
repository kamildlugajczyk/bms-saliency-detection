import io
import PySimpleGUIQt as sg
import os
from PIL import Image

file_types = (("JPG", "*.jpg"), ("PNG", "*.png"), ("BITMAP", "*.bmp"),)

left_column = [[sg.Image(key="-IMAGE BEFORE-")]]
right_column = [[sg.Image(key="-IMAGE AFTER-")]]
layout = [
    [sg.Text("Choose a file: "), sg.In(enable_events=True, key="-FILE-"), sg.FileBrowse(file_types=file_types)],
    [sg.Button("Process image")],
    [sg.Column(left_column), sg.VSeperator(), sg.Column(right_column)]
]

window = sg.Window('Saliency detection using BMS', layout, size=(1080, 600))

if __name__ == '__main__':
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == "-FILE-":
            path = values["-FILE-"]
            if os.path.exists(path):
                image = Image.open(path)
                image.thumbnail((600, 600))
                image_bytes = io.BytesIO()
                image.save(image_bytes, format="PNG")
                window["-IMAGE BEFORE-"].update(data=image_bytes.getvalue())

        # if event == "Process image":
          # invoke bms
          # window["-IMAGE AFTER-"].update(data=<bytes>)

    window.close()
