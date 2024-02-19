from findCurve import *

from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

######################################
## actions ###########################
######################################

# select a file from the computer, print it to the textbox and store value in PATH
def action_selectFiles(textbox):
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("CSV Files","*.csv"),
                                                       ("all files", "*.*")))
    # Change label contents
    textbox.insert(INSERT, filename)
    textbox.see(END)
    PATH = filename


def action_getDataAndDisplay(
        textbox, canvasFrame, tb_logWindow, canvas_size = (350, 450)):
    # reset frame
    for widget in canvasFrame.winfo_children():
        widget.destroy()

    inputFilePath = textbox.get("1.0", "end-1c")
    tb_logWindow.insert(END, "LOG open file: " + inputFilePath +"\n")
    tb_logWindow.see(END)

    global PATH, WAVELENGTH_MAP, DATA

    # extract data from the file
    try:
       w, d = extractDataFromPixis(inputFilePath, tb_logWindow)
       # from this point onward, the global variables should not be changed
       PATH = inputFilePath 
       WAVELENGTH_MAP = w
       DATA = d
       tb_logWindow.insert(END, "LOG data extraction successful...\n")   
    except FileNotFoundError:
       tb_logWindow.config(fg = "red")
       tb_logWindow.insert(END, "ERR cannot find file \n")
       return

    # plot raw data
    try:
        tb_logWindow.insert(END, "LOG creating plot ...\n")
        print("DATA: ", DATA)
        print("WL: ", WAVELENGTH_MAP)
        fig_raw = plot_rawData(np.array(DATA), np.array(WAVELENGTH_MAP))
        tb_logWindow.insert(END, "LOG generating figure...\n")
        fig_raw.subplots_adjust(left = -1, bottom = 0.13)
    except:
       tb_logWindow.config(fg = "red")
       tb_logWindow.insert(END, "ERR cannot plot raw data \n")
       return
    tb_logWindow.see(END)

    # update canvas frame
    try:
        canvas = generate_canvas(fig_raw, canvasFrame)
        canvas.config(width = canvas_size[0], height = canvas_size[1]-50)
        canvas.pack()
    except:
       tb_logWindow.config(fg = "red")
       tb_logWindow.insert(END, "ERR cannot update canvas\n")
       return

    tb_logWindow.insert(END, "LOG raw data imported successfully\n")
    tb_logWindow.see(END)


def action_curveDetectAndDisplay(
        canvasFrame, tb_logWindow, canvas_size = (350, 450)):

    # reset frame
    for widget in canvasFrame.winfo_children():
        widget.destroy()

    tb_logWindow.insert(END, "LOG finding curvatures...\n")
    tb_logWindow.see(END)

    if len(DATA) == 0 or len(WAVELENGTH_MAP) == 0:
        tb_logWindow.config(fg = "red")
        tb_logWindow.insert(END, "ERR please select a raw data set first\n")
        return

    # find curve
    try:
        fig = findCurve(DATA, WAVELENGTH_MAP)
        fig.subplots_adjust(left = -1, bottom = 0.13)
    except:
        tb_logWindow.config(fg = "red")
        tb_logWindow.insert(END, "ERR cannot update canvas\n")
        return

    # update canvas frame
    try:
        canvas = generate_canvas(fig, canvasFrame)
        canvas.config(width = canvas_size[0], height = canvas_size[1]-50)
        canvas.pack()
    except:
       tb_logWindow.config(fg = "red")
       tb_logWindow.insert(END, "ERR cannot update resulting canvas\n")
       return

    tb_logWindow.insert(END, "LOG detection finished\n")
    tb_logWindow.see(END)

######################################
## canvas ############################
######################################
def generate_canvas(fig, frame):
    # creating the Tkinter canvas, containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = frame)  
    canvas.draw()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    return canvas.get_tk_widget()
    
