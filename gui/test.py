import tkinter as tk
import re

window = tk.Tk()
cropPixelRange = tk.StringVar(value = "[min, max]")
en_cPixelRange = tk.Entry(window, textvariable=cropPixelRange)

def testGettingIntFromStringVar():
    print(cropPixelRange.get())
    num = [int(s) for s in re.findall(r'\d+', cropPixelRange.get())]
    print(num[:2])

btn = tk.Button(text="TEST", command = testGettingIntFromStringVar)
en_cPixelRange.pack()
btn.pack()


tk.mainloop()