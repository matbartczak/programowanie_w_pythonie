from Converter import Converter
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
import time


root = tk.Tk()

# ---------- Window size & centering ----------
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 250

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (WINDOW_WIDTH // 2)
y = (screen_height // 2) - (WINDOW_HEIGHT // 2)

root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
root.resizable(False, False)
root.title("File Converter")

# ---------- Grid configuration ----------
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

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
        filename = os.path.basename(converter.get())
        label.config(text= f"Wybrany plik: {filename}")
        btn_cancel.grid(row=2, column=0, columnspan=2, pady=10)

        if "mobi" in filename:
            btn_convert_to_epub.grid(row=3, column=0, padx=50, pady=10, sticky="ew")
            btn_convert_to_pdf.grid(row=3, column=1, padx=50, pady=10, sticky="ew")
        elif "epub" in filename:
            btn_convert_to_mobi.grid(row=3, column=0, padx=50, pady=10, sticky="ew")
            btn_convert_to_pdf.grid(row=3, column=1, padx=50, pady=10, sticky="ew")
        elif "pdf" in filename:
            btn_convert_to_mobi.grid(row=3, column=0, padx=50, pady=10, sticky="ew")
            btn_convert_to_epub.grid(row=3, column=1, padx=50, pady=10, sticky="ew")
        else:
            label.config(text= f"Wybrano plik o nieobsługiwanym formacie.")

def run_conversion(input_f, output_f):

    label.config(text= "Trwa konwersja...")
    if input_f == 'epub' and output_f == 'mobi':
        converter.from_epub('mobi')
    elif input_f == 'epub' and output_f == 'pdf':
        converter.from_epub('pdf')
    elif input_f == 'mobi' and output_f == 'epub':
        converter.from_mobi('epub')
    elif input_f == 'mobi' and output_f == 'pdf':
        converter.from_mobi('pdf')
    elif input_f == 'pdf' and output_f == 'mobi':
        converter.from_pdf('mobi')
    elif input_f == 'pdf' and output_f == 'epub':
        converter.from_pdf('epub')

    label.config(text= "")
    root.after(0, stop_progress)
    btn_cancel.grid_remove()
    btn_convert_to_mobi.grid_remove()
    btn_convert_to_epub.grid_remove()
    btn_convert_to_pdf.grid_remove()

def stop_progress():
    progress.stop()
    progress.grid_remove()

def ToMobi():
    input_file = "epub" if "epub" in converter.get() else "pdf"

    progress.grid(row=4, column=0, columnspan=2, pady=10)
    progress.start(10)

    thread = threading.Thread(
        target=run_conversion,
        args=(input_file, "mobi"),
        daemon=True
    )
    thread.start()

def ToPdf():
    input_file = "epub" if "epub" in converter.get() else "mobi"

    progress.grid(row=4, column=0, columnspan=2, pady=10)
    progress.start(10)

    thread = threading.Thread(
        target=run_conversion,
        args=(input_file, "pdf"),
        daemon=True
    )
    thread.start()

def ToEpub():
    input_file = "mobi" if "mobi" in converter.get() else "pdf"

    progress.grid(row=4, column=0, columnspan=2, pady=10)
    progress.start(10)

    thread = threading.Thread(
        target=run_conversion,
        args=(input_file, "epub"),
        daemon=True
    )
    thread.start()

def CancelAction():
    label.config(text="Anulowano")
    btn_cancel.grid_remove()
    btn_convert_to_mobi.grid_remove()
    btn_convert_to_epub.grid_remove()
    btn_convert_to_pdf.grid_remove()


label = tk.Label(root, text="")
label.grid(row=0, column=0, columnspan=2, pady=20)

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=300,
    mode="indeterminate"
)

button = tk.Button(root, text='Otwórz plik', command=UploadAction)
button.grid(row=1, column=0, columnspan=2, pady=10)

btn_cancel = tk.Button(root, text="Anuluj", command=CancelAction)

btn_convert_to_mobi = tk.Button(root, text="MOBI", command=ToMobi)
btn_convert_to_epub = tk.Button(root, text="EPUB", command=ToEpub)
btn_convert_to_pdf = tk.Button(root, text="PDF", command=ToPdf)

root.mainloop()
