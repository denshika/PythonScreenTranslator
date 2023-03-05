import tkinter as tk
from tkinter import ttk
import keyboard
import pytesseract
from googletrans import Translator
from mss import mss
import numpy as np
from PIL import Image
import time
import pystray
from threading import Thread
import pidfile

shouldExit = False

# The key is the display name
# The first value is the pytesseract one
# The second value is the googletrans one
languages = {
    "Auto": (),
    "French": ("fra", "fr"),
    "English": ("eng", "en"),
    "German": ("deu", "de"),
    "Japanese": ("jpn", "ja"),
    "Simplified Chinese": ("chi-sim", "zh-cn"),
    "Traditional Chinese": ("chi-tra", "zh-tw")
}

fromSelectedLanguage = "Auto"
toSelectedLanguage = "Auto"

class LanguageSelection:
    def __init__(self):
        self.root = tk.Tk()

        self.fromLabel = tk.Label(self.root, text="from")
        self.fromLabel.pack()

        self.fromStringVar = tk.StringVar()
        self.fromComboBox = ttk.Combobox(self.root, state="readonly", textvariable=self.fromStringVar, values=list(languages.keys()))
        self.fromComboBox.current(0)
        self.fromComboBox.pack(padx=10, pady=(2, 5))

        self.toLabel = tk.Label(self.root, text="from")
        self.toLabel.pack()

        self.toStringVar = tk.StringVar()
        self.toComboBox = ttk.Combobox(self.root, state="readonly", textvariable=self.toStringVar, values=list(languages.keys()))
        self.toComboBox.current(0)
        self.toComboBox.pack(padx=10, pady=(2, 5))

        self.validButton = tk.Button(self.root, text="valid", command=self.onValid)
        self.validButton.pack(padx=10, pady=5)

        self.root.bind('<Return>', self.onEnterPress)
        self.root.mainloop()

    def onEnterPress(self, x):
        self.onValid()

    def onValid(self):
        global fromSelectedLanguage
        fromSelectedLanguage = self.fromStringVar.get()
        global toSelectedLanguage
        toSelectedLanguage = self.toStringVar.get()
        self.root.destroy()

class SelectionWindow:
    def __init__(self):
        self.root = tk.Tk()

        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.2)
        self.root.attributes('-topmost', True)
        self.root.config(cursor="tcross")

        self.firstScreenPosition = (0, 0)

        self.root.bind("<Button-1>", self.onLeftButtonClick)
        self.root.bind("<ButtonRelease-1>", self.onLeftButtonRelease)

        self.root.after(1, self.loop)
        self.root.mainloop()

    def loop(self):
        global shouldExit
        if keyboard.is_pressed('esc') or shouldExit:
            self.root.destroy()
            return

        self.root.after(1, self.loop)

    def onLeftButtonClick(self, event):
        self.firstScreenPosition = (event.x, event.y)

    def onLeftButtonRelease(self, event):
        secondScreenPosition = (event.x, event.y)
        self.root.destroy()
        x0 = min(self.firstScreenPosition[0], secondScreenPosition[0])
        y0 = min(self.firstScreenPosition[1], secondScreenPosition[1])
        x1 = max(self.firstScreenPosition[0], secondScreenPosition[0])
        y1 = max(self.firstScreenPosition[1], secondScreenPosition[1])
        ResultWindow(x0, y0, x1, y1)




class ResultWindow:
    def __init__(self, x0, y0, x1, y1):
        self.root = tk.Tk()

        imageArray = np.array(mss().grab({'top': y0, 'left': x0, 'width': x1 - x0, 'height': y1 - y0}))
        image = Image.fromarray(imageArray)

        if (fromSelectedLanguage == "Auto"):
            baseText = pytesseract.image_to_string(image)
        else:
            baseText = pytesseract.image_to_string(image, config='-l ' + languages[fromSelectedLanguage][0])

        if (baseText != ""):
            translationResult = None
            if (fromSelectedLanguage == "Auto"):
                translationResult = Translator().translate(baseText)
            else:
                translationResult = Translator().translate(baseText, src=languages[fromSelectedLanguage][1], dest=languages[toSelectedLanguage][1])

            tk.Label(self.root, text=f"Base text: {translationResult.src}\n{baseText}\nTranslated text: {translationResult.dest}\n{translationResult.text}").pack()
        else:
            tk.Label(self.root, text="Couldn't find any text to translate").pack()

        self.root.after(1, self.loop)
        self.root.mainloop()

    def loop(self):
        global shouldExit
        if keyboard.is_pressed('esc') or shouldExit:
            self.root.destroy()
            return

        self.root.after(1, self.loop)

def mainloop():
    while True:
        if keyboard.is_pressed('ctrl+t'):
            SelectionWindow()
        if shouldExit:
            break
        time.sleep(0.01)

def onExitClicked(icon, item):
    global shouldExit
    shouldExit = True
    icon.stop()

def main():
    LanguageSelection()

    Thread(target=mainloop).start()

    pystray.Icon(
        'japanese translator',
        Image.open("icon.png"),
        menu=pystray.Menu(
            pystray.MenuItem(
                'exit',
                onExitClicked
            )
        )
    ).run()


try:
    with pidfile.PIDFile():
        main()
except pidfile.AlreadyRunningError:
    exit()
