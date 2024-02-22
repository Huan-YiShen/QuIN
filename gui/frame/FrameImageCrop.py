import tkinter as tk
import ntpath
import numpy as np
import matplotlib.pyplot as plt

from frame.FrameCanvas import FrameCanvas
from process.generatePlot import plot_rawData

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class FrameImageCrop(tk.Frame):
    pass