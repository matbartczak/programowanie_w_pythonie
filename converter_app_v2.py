from Converter import Converter
import os
import tkinter as tk
from tkinter import filedialog
import threading
import subprocess

#KONFIGURACJA OKNA
root = tk.Tk()
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 370

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (WINDOW_WIDTH // 2)
y = (screen_height // 2) - (WINDOW_HEIGHT // 2)

root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
root.resizable(False, False)
root.title("Konwerter e-booków")
root.configure(bg="#e0e0e0")
root.columnconfigure(0, weight=1)

converter = Converter()

#NAGŁÓWEK
title_label = tk.Label(
    root,
    text="Konwerter e-booków",
    font=("Segoe UI", 18, "bold"),
    bg="#e0e0e0",
    fg="#222222"
)
title_label.grid(row=0, column=0, pady=(15,0))

subtitle_label = tk.Label(
    root,
    text="EPUB • MOBI • PDF",
    font=("Segoe UI", 10),
    fg="#222222",
    bg="#e0e0e0"
)
subtitle_label.grid(row=1, column=0, pady=(0,15))

#STATUS PLIKU
file_info_label = tk.Label(
    root,
    text="Nie wybrano pliku",
    font=("Segoe UI", 9),
    fg="#222222",
    bg="#e0e0e0"
)
file_info_label.grid(row=3, column=0, pady=(2,10))

#PRZYCISK WYBIERZ PLIK
def UploadAction():
    filename = filedialog.askopenfilename(
        title="Wybierz plik",
        filetypes=(
            ("PDF files", "*.pdf"),
            ("MOBI files", "*.mobi"),
            ("EPUB files", "*.epub"),
            ("all files","*.*")
        )
    )
    if not filename:
        return

    converter.set(filename)
    name = os.path.basename(filename)
    file_info_label.config(text=f"Wybrany plik: {name}")

    # ukryj przyciski i status konwersji
    convert_label.pack_forget()
    btn_convert_to_mobi.pack_forget()
    btn_convert_to_epub.pack_forget()
    btn_convert_to_pdf.pack_forget()
    conversion_status_label.pack_forget()
    btn_cancel.pack_forget()
    progress_frame.pack_forget()

    # pokaż przyciski konwersji
    convert_label.pack(side="top", pady=(0,5))
    if name.endswith(".mobi"):
        btn_convert_to_epub.pack(side="left", padx=5)
        btn_convert_to_pdf.pack(side="left", padx=5)
    elif name.endswith(".epub"):
        btn_convert_to_mobi.pack(side="left", padx=5)
        btn_convert_to_pdf.pack(side="left", padx=5)
    elif name.endswith(".pdf"):
        btn_convert_to_mobi.pack(side="left", padx=5)
        btn_convert_to_epub.pack(side="left", padx=5)

    btn_cancel.pack(pady=(10,0))

button = tk.Button(
    root,
    text="📂 Wybierz plik",
    font=("Segoe UI", 12, "bold"),
    bg="#222222",
    fg="white",
    bd=0,
    padx=20,
    pady=8,
    cursor="hand1",
    command=UploadAction
)
button.grid(row=2, column=0, pady=10)

#FRAME NA PRZYCISKI KONWERSJI
buttons_frame = tk.Frame(root, bg="#e0e0e0")
buttons_frame.grid(row=4, column=0, pady=5)

convert_label = tk.Label(
    buttons_frame,
    text="Konwertuj do:",
    font=("Segoe UI", 11, "bold"),
    bg="#e0e0e0",
    fg="#222222"
)
convert_label.pack_forget()

conversion_status_label = tk.Label(
    buttons_frame,
    text="",
    font=("Segoe UI", 10, "bold"),
    bg="#e0e0e0",
    fg="#222222"
)
conversion_status_label.pack_forget()

def make_convert_button(text, command):
    return tk.Button(
        buttons_frame,
        text=text,
        font=("Segoe UI", 10, "bold"),
        bg="#222222",
        fg="white",
        bd=0,
        padx=45,
        pady=3,
        cursor="hand1",
        command=command
    )

btn_convert_to_mobi = make_convert_button("MOBI", lambda: start_thread("mobi"))
btn_convert_to_epub = make_convert_button("EPUB", lambda: start_thread("epub"))
btn_convert_to_pdf  = make_convert_button("PDF",  lambda: start_thread("pdf"))

btn_convert_to_mobi.pack_forget()
btn_convert_to_epub.pack_forget()
btn_convert_to_pdf.pack_forget()

# PRZYCISK ANULUJ
cancel_frame = tk.Frame(root, bg="#e0e0e0")
cancel_frame.grid(row=5, column=0, pady=20)

btn_cancel = tk.Button(
    cancel_frame,
    text="Anuluj",
    font=("Segoe UI", 10, "bold"),
    bg="#a0a0a0",
    fg="#222222",
    bd=0,
    padx=15,
    pady=5,
    cursor="hand1",
    command=lambda: CancelAction()
)
btn_cancel.pack()
btn_cancel.pack_forget()

# PASEK POSTĘPU
progress_frame = tk.Frame(buttons_frame, bg="#e0e0e0")
progress_frame.pack_forget()
progress_canvas = tk.Canvas(progress_frame, width=300, height=20, bg="#d0d0d0", highlightthickness=0)
progress_canvas.pack(side="left")
progress_label = tk.Label(progress_frame, text="0%", font=("Segoe UI", 10), bg="#e0e0e0", fg="#222222")
progress_label.pack(side="right", padx=5)

def update_progress(value):
    progress_canvas.delete("all")
    bar_width = int(300 * value / 100)
    progress_canvas.create_rectangle(0, 0, bar_width, 20, fill="black")
    progress_label.config(text=f"{value}%")
    root.update_idletasks()

# LOGIKA KONWERSJI
def run_conversion(input_f, output_f):
    conversion_status_label.pack(side="top", pady=(5,0))
    conversion_status_label.config(text="Trwa konwersja...")

    btn_convert_to_mobi.pack_forget()
    btn_convert_to_epub.pack_forget()
    btn_convert_to_pdf.pack_forget()
    convert_label.pack_forget()

    # pokaż pasek postępu
    progress_frame.pack(side="top", pady=(5,5))
    update_progress(0)

    fname = converter.get()
    output_path = os.path.join(os.getcwd(), f"{os.path.splitext(os.path.basename(fname))[0]}.{output_f}")

    cmd = ["ebook-convert", fname, output_path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        if "%" in line:
            try:
                perc = int(line.strip().split("%")[0].split()[-1])
                root.after(0, lambda p=perc: update_progress(p))
            except:
                continue

    process.wait()
    root.after(0, conversion_finished)

def conversion_finished():
    conversion_status_label.config(text="Gotowe!")
    btn_cancel.pack_forget()
    update_progress(100)

def start_thread(output_format):
    fname = converter.get()
    if not fname:
        return
    if fname.endswith(".epub"):
        input_format = "epub"
    elif fname.endswith(".mobi"):
        input_format = "mobi"
    elif fname.endswith(".pdf"):
        input_format = "pdf"

    thread = threading.Thread(
        target=run_conversion,
        args=(input_format, output_format),
        daemon=True
    )
    thread.start()

def CancelAction():
    file_info_label.config(text="Anulowano")
    btn_convert_to_mobi.pack_forget()
    btn_convert_to_epub.pack_forget()
    btn_convert_to_pdf.pack_forget()
    btn_cancel.pack_forget()
    convert_label.pack_forget()
    conversion_status_label.pack_forget()
    progress_frame.pack_forget()

root.mainloop()