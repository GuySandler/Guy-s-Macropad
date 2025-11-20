import board
import busio
import displayio
import adafruit_ssd1306
from adafruit_display_text import label
import terminalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros, Delay

displayio.release_displays()
i2c = busio.I2C(board.GP7, board.GP6)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_ssd1306.SSD1306(display_bus, width=128, height=32)

splash = displayio.Group()
display.show(splash)

text_area = label.Label(terminalio.FONT, text="Ready", color=0xFFFFFF, x=0, y=10)
splash.append(text_area)

texts = []
command_macros = []

def add_key(gpio, command, display_text):
    taps = [KC.LCTRL(KC.LALT(KC.T)), Delay(500)] # control alt t
    for char in command:
        if char == ' ':
            taps.append(Tap(KC.SPACE))
        elif char == '-':
            taps.append(Tap(KC.MINUS))
        else:
            key = getattr(KC, char.upper())
            taps.append(Tap(key))
    taps.append(Tap(KC.ENTER))
    macro = KC.MACRO(*taps)
    command_macros.append(macro)
    texts.append(display_text)
    PINS.append(gpio)

# GPIO button map like the pcb:
# 26 27 3 4
# 28 29 2 1
PINS = []

# Add keys
add_key(board.GP26, "ls", "ls")
add_key(board.GP27, "code", "Opening Vscode")
add_key(board.GP3, "steam", "Opening Steam")
add_key(board.GP4, "discord", "Opening Discord")

add_key(board.GP28, "nvim", "Opening Neovim")
add_key(board.GP29, "", "idk")
add_key(board.GP2, "top", "top")
add_key(board.GP1, "sleep", "Sleep")

class MyKeyboard(KMKKeyboard):
    def on_press(self, key, keyboard, *args, **kwargs):
        super().on_press(key, keyboard, *args, **kwargs)
        if key in command_macros:
            idx = command_macros.index(key)
            text_area.text = texts[idx]

keyboard = MyKeyboard()

macros = Macros()
keyboard.modules.append(macros)

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

keyboard.keymap = command_macros

if __name__ == '__main__':
    keyboard.go()