import io
import PySimpleGUIQt as sg
import os
from PIL import Image
from bms import bms

file_types = (("JPG", "*.jpg"), ("PNG", "*.png"), ("BITMAP", "*.bmp"),)

left_column = [[sg.Image(key="-IMAGE BEFORE-")]]
right_column = [[sg.Image(key="-IMAGE AFTER-")]]
layout = [
    [sg.Text("Choose a file: "), sg.In(enable_events=True, key="-FILE-"), sg.FileBrowse(file_types=file_types)],
    [sg.Button("Process image")],
    [sg.Column(left_column), sg.VSeperator(), sg.Column(right_column)]
]

window = sg.Window('Saliency detection using BMS', layout, size=(1080, 600))

path = ""
result_path = "../results/result.jpg"


def get_image_data(path, max_size=(600, 400), save=False):
    img = Image.open(path)
    img.thumbnail(max_size)
    if save:
        img.save(result_path)

    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


if __name__ == '__main__':
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == "-FILE-":
            path = values["-FILE-"]
            if os.path.exists(path):
                before = get_image_data(path, save=True)
                window["-IMAGE BEFORE-"].update(data=before)

        if event == "Process image":
            if path != "":
                bms.process(result_path)
                after = get_image_data(result_path)
                window["-IMAGE AFTER-"].update(data=after)

    window.close()
