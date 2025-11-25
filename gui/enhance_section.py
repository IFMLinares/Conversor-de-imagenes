import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from image_tools.tools import enhance_image
from .utils import show_image_preview

def show_enhance_section(main_frame):
    def select_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.webp")])
        if file_path:
            entry_image_path.delete(0, ctk.END)
            entry_image_path.insert(0, file_path)
            show_image_preview(file_path, preview_label)

    def enhance():
        input_path = entry_image_path.get()
        output_name = entry_output_name.get()
        width = entry_width.get()
        height = entry_height.get()
        sharpen = sharpen_var.get()
        if not input_path or not output_name:
            messagebox.showerror("Error", "Selecciona una imagen y escribe el nombre de salida")
            return
        try:
            w = int(width) if width else None
            h = int(height) if height else None
            output_path = f"{output_name}_mejorada.png"
            enhance_image(input_path, output_path, width=w, height=h, sharpen=sharpen)
            messagebox.showinfo("Éxito", f"Imagen mejorada guardada como {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mejorar la imagen: {e}")

// Archivo eliminado: sección de mejorar calidad
