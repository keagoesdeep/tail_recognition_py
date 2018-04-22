from tkinter import *
import colorsys

UPPER_YELLOW = "upper_yellow"

LOW_YELLOW = "low_yellow"

UPPER_BLUE = "upper_blue"

LOW_BLUE = "low_blue"

UPPER_RED = "upper_red"

LOW_RED = "low_red"

DEFAULT_COLOR_RANGES = {LOW_RED: {"hue": 300, "saturation": 15, "value": 20},
                        UPPER_RED: {"hue": 360, "saturation": 100, "value": 100},
                        LOW_BLUE: {"hue": 200, "saturation": 50, "value": 16},
                        UPPER_BLUE: {"hue": 280, "saturation": 100, "value": 100},
                        LOW_YELLOW: {"hue": 50, "saturation": 16, "value": 15},
                        UPPER_YELLOW: {"hue": 90, "saturation": 100, "value": 100}}


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h / 360, s / 100, v / 100))


def dec2hex(number):
    return '{:02x}'.format(int(number))


class CameraSettings:

    def __init__(self):
        self._root = None
        self._scales = {}

    def init_ui(self):
        self._root = Tk()

        self._create_colour_picker("Red lower boundary", starting_row=0, column=0, key=LOW_RED)
        self._create_colour_picker("Red upper boundary", starting_row=0, column=1, key=UPPER_RED)

        self._create_colour_picker("Blue lower boundary", starting_row=4, column=0, key=LOW_BLUE)
        self._create_colour_picker("Blue upper boundary", starting_row=4, column=1, key=UPPER_BLUE)

        self._create_colour_picker("Yellow lower boundary", starting_row=8, column=0, key=LOW_YELLOW)
        self._create_colour_picker("Yellow upper boundary", starting_row=8, column=1, key=UPPER_YELLOW)

        self._root.mainloop()

    def _hue_callback(self, event, key, label):
        selected_color = self._scales[key]
        selected_color["hue"] = int(event)
        rgb = hsv2rgb(selected_color["hue"], selected_color["saturation"], selected_color["value"])
        hex_rgb = "#" + "".join([dec2hex(dec) for dec in rgb])
        label.config(bg=hex_rgb)

    def _saturation_callback(self, event, key, label):
        selected_color = self._scales[key]
        selected_color["saturation"] = int(event)
        rgb = hsv2rgb(selected_color["hue"], selected_color["saturation"], selected_color["value"])
        hex_rgb = "#" + "".join([dec2hex(dec) for dec in rgb])
        label.config(bg=hex_rgb)

    def _value_callback(self, event, key, label):
        selected_color = self._scales[key]
        selected_color["value"] = int(event)
        rgb = hsv2rgb(selected_color["hue"], selected_color["saturation"], selected_color["value"])
        hex_rgb = "#" + "".join([dec2hex(dec) for dec in rgb])
        label.config(bg=hex_rgb)

    def _create_colour_picker(self, label_message, starting_row, column, key):
        # self._scales[key] = {"hue": 0, "saturation": 0, "value": 0}
        self._scales[key] = DEFAULT_COLOR_RANGES[key]

        label = Label(self._root, text=label_message, bg="green")
        label.grid(row=starting_row, column=column)

        scale = Scale(self._root, from_=0, to=360, orient=HORIZONTAL, label="Hue",
                      command=lambda event: self._hue_callback(event, key, label))
        scale.set(self._scales[key]["hue"])
        scale.grid(row=starting_row + 1, column=column)

        scale = Scale(self._root, from_=0, to=100, orient=HORIZONTAL, label="Saturation",
                      command=lambda event: self._saturation_callback(event, key, label))
        scale.set(self._scales[key]["saturation"])
        scale.grid(row=starting_row + 2, column=column)

        scale = Scale(self._root, from_=0, to=100, orient=HORIZONTAL, label="Value",
                      command=lambda event: self._value_callback(event, key, label))
        scale.set(self._scales[key]["value"])
        scale.grid(row=starting_row + 3, column=column)

    def get_values(self, key):
        return self._scales[key]
