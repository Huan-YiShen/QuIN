# from gui_actions import *
from tkinter import *

from findCurve import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
##### This is a functional approach of the draft GUI version 1
##### version 2 will be built using object orientated program

######################################
## global parameter ##################
######################################
WAVELENGTH_MAP = [] # row dhat indicate the wavelength of the spectrometer
DATA = [] # intensity value of a 2D array (transposed)
PATH = "" # file path

# layout
row = 1
col = 1
colFullSpan = 3
canvas_width = 350
canvas_height = 450
# store Tk() is the window variable
window = Tk()
tb_logWindow = Text(window, height = 5, width = 96, wrap=NONE, bg = "ivory2")
frame_canvas_raw = Frame(window, bg="black", borderwidth=2, width = canvas_width, height = canvas_height)
frame_canvas_curve = Frame(window, bg="black",  borderwidth=2, width = canvas_width, height = canvas_height)

######################################
## frame #############################
######################################
def create_selectFile_frame():
    frame_selectFile = Frame(window, bg="#ababab")
    label_file_explorer = Label(frame_selectFile, text = "Select you files:")

    h=Scrollbar(frame_selectFile, orient='horizontal')
    tb_fileSelect = Text(frame_selectFile, height = 1, width = 84,  
                        wrap=NONE, xscrollcommand=h.set)
    tb_fileSelect.insert(INSERT, "C:/Users/James/Documents/UWaterloo/QuIN/QuIN - GitHub/imageAnalysis/labData/2023_11_15_Image Data-new_FW/2023_11_15_Image Data-new_FW/FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv")
    tb_fileSelect.see(END)

    btn_fileGet = Button(frame_selectFile,
                            text = "≡",
                            command = lambda: action_selectFiles(tb_fileSelect))

    btn_fileSelect = Button(frame_selectFile,
                            text = "SELECT FILE", fg = "black", bg = "lemon chiffon",
                            command = lambda: action_getDataAndDisplay(
                                tb_fileSelect, frame_canvas_raw, tb_logWindow, (canvas_width, canvas_height)))

    label_file_explorer.grid(row = 1, column = 1)
    tb_fileSelect.grid(row = 1, column = 2, columnspan=2)
    btn_fileGet.grid(row = 1, column = 4)
    btn_fileSelect.grid(row = 1, column = 5)
    return frame_selectFile


def create_display_detect_frame():
    frame_rt = Frame(window, bg="#ababab")

    btn_detect = Button(frame_rt, text = "DETECT",
                        command = lambda: action_curveDetectAndDisplay(
                            frame_canvas_curve, tb_logWindow, (canvas_width, canvas_height)))
    btn_detect.grid(column = 1, row = 1)

    return frame_rt

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


######################################
## MAIN ##############################
######################################
window.title('Curvature Detection')
window.geometry("1000x600")
window.config(background = "white")


# windows widgets
label_title = Label(master = window, text = "curvature detection")
frame_selectFile = create_selectFile_frame()
frame_detect = create_display_detect_frame()

# row 1
label_title.grid(column = col, row = row, columnspan= colFullSpan)

# row 2
row += 1
col = 1
frame_selectFile.grid(column = col, row = row, columnspan= colFullSpan)

# row 3
row += 1
col = 1
frame_canvas_raw.grid(column = col, row = row)
col += 1
frame_detect.grid(column = col, row = row)
col += 1
frame_canvas_curve.grid(column = col, row = row)

# row 4
row += 1
col = 1
tb_logWindow.grid(column = col, row = row, columnspan= colFullSpan)

window.mainloop()