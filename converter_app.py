from Converter import Converter
import tkinter as tk
from tkinter import filedialog

converter = Converter()

def UploadAction(event= None):
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("EPUB files",
                                                        "*.epub*"),
                                                        ("MOBI files",
                                                        "*.mobi*"),
                                                        ("PDF files",
                                                        "*.pdf*"),
                                                       ("all files",
                                                        "*.*")))
    if filename:
        converter.set(filename)

root = tk.Tk()


button = tk.Button(root, text='Open', command=UploadAction)
button.pack()

root.mainloop()