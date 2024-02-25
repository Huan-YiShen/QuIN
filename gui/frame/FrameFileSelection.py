import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class FrameFileSelection(ttk.Frame):
    def __init__(self, parent, selectedPath : tk.StringVar.__class__):
        super().__init__(parent)
        self.selectedPath = selectedPath
        self.create_widgets()
        self.place_widgets()


    def create_widgets(self):
        self.label_file_explorer = tk.Label(self, text = "Select files:")

        h = tk.Scrollbar(self, orient='horizontal')
        self.textbox = tk.Text(
            self, height = 1, wrap=tk.NONE, xscrollcommand=h.set)
        # demo
        self.textbox.insert(
            tk.INSERT, "../imageAnalysis/labData/2023_11_15_Image Data-new_FW/2023_11_15_Image Data-new_FW/FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv") # for debug
        self.textbox.see(tk.END)

        # selection buttons
        self.btn_fileGet = tk.Button(
            self, text = "≡", borderwidth = 2, 
            command = lambda: self.action_selectFiles())
        self.btn_select = tk.Button(
            self, text = "SELECT FILE", fg = "black", bg = "lemon chiffon", borderwidth=2, 
            command = lambda: self.selectedPath.set(self.textbox.get("1.0", "end-1c")))


    def place_widgets(self):
        self.columnconfigure(1, weight=1)
        # layout 
        self.label_file_explorer.grid(row = 0, column = 0)
        self.textbox.grid(row = 0, column = 1, sticky="we")
        self.btn_fileGet.grid(row = 0, column = 2)
        self.btn_select.grid(row = 0, column = 3)


    def action_selectFiles(self):
        filename = filedialog.askopenfilename(
            initialdir = "/", title = "Select a File",
            filetypes = (("CSV Files","*.csv"), ("all files", "*.*")))
        # Change label contents
        if (filename):
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.INSERT, filename)
            self.textbox.see(tk.END)