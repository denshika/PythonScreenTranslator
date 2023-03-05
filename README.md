# PythonScreenTranslator
Little python script to translate text on your screen

# How to use
* Run the main.py script (be sure icon.png is in the same directory)
* A language selection window should pop up, choose what language you want (Auto doesn't work for languages with non latin alphabet)
* Once it's done press enter or click the valid button
* A little icon (system stray) should pop up somewhere on your taskbar, if you wan't to quit the script just right click on it and select "exit"
* Press ctrl+t to take a screenshot, it should open a blank window
* Drag from the first point of selection to the second with left click
* Once left click is released a window should open with the translation of the text

# Dependencies
* Tesseract-OCR for recognizing text on image
  * https://github.com/tesseract-ocr/tesseract (pre-built: https://github.com/UB-Mannheim/tesseract/wiki)
  * `pip install pytesseract`
* googletrans for translating text
  * `pip install googletrans`
* numpy for some manipulation of images
  * `pip install numpy`
* keyboard for keyboard inputs
  * `pip install keyboard`
* tkinter for window management
  * `pip install tk`
* mss for screenshot
  * `pip install mss`
* pillow for images manipulation
  * `pip install pillow`
* pystray for system stray (little icons on the right of the taskbar (on Windows))
  * `pip install pystray`
* pidfile for avoiding launching multiple time the script
  * `pip install python-pidfile`
