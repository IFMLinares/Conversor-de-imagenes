import threading

def show_progress_bar(parent, row, columnspan=3):
    progress_bar = ctk.CTkProgressBar(parent, width=400)
    progress_bar.grid(row=row, column=0, columnspan=columnspan, padx=10, pady=5)
    progress_bar.set(0)
    progress_label = ctk.CTkLabel(parent, text="0%", width=50)
    progress_label.grid(row=row, column=columnspan, padx=10, pady=5)
    progress_bar.grid_remove()
    progress_label.grid_remove()
    return progress_bar, progress_label

def run_with_progress(task, progress_bar, progress_label, parent, steps=10):
    def worker():
        progress_bar.grid()
        progress_label.grid()
        parent.update_idletasks()
        import time
        for i in range(1, 101, int(100/steps)):
            progress_bar.set(i/100)
            progress_label.configure(text=f"{i}%")
            parent.update_idletasks()
            time.sleep(0.05)
        try:
            task()
            progress_bar.set(1)
            progress_label.configure(text="100%")
        except Exception:
            progress_bar.set(0)
            progress_label.configure(text="0%")
        time.sleep(0.5)
        progress_bar.grid_remove()
        progress_label.grid_remove()
    threading.Thread(target=worker).start()
from PIL import Image
import customtkinter as ctk

def show_image_preview(file_path, label, size=(200, 200)):
    try:
        img = Image.open(file_path)
        img.thumbnail(size)
        img_tk = ctk.CTkImage(light_image=img, size=(img.width, img.height))
        label.configure(image=img_tk, text="")
        label.image = img_tk
    except Exception:
        label.configure(text="No se pudo cargar la imagen", image=None)
