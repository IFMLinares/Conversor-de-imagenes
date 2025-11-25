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

    label_image = ctk.CTkLabel(main_frame, text="Seleccionar Imagen:")
    label_image.grid(row=0, column=0, padx=10, pady=10)
    entry_image_path = ctk.CTkEntry(main_frame, width=500)
    entry_image_path.grid(row=0, column=1, padx=10, pady=10)
    button_search = ctk.CTkButton(main_frame, text="Buscar", command=select_image)
    button_search.grid(row=0, column=2, padx=10, pady=10)

    label_output = ctk.CTkLabel(main_frame, text="Nombre de la Imagen Nueva:")
    label_output.grid(row=1, column=0, padx=10, pady=10)
    entry_output_name = ctk.CTkEntry(main_frame, width=500)
    entry_output_name.grid(row=1, column=1, padx=10, pady=10)

    label_width = ctk.CTkLabel(main_frame, text="Nuevo Ancho (opcional):")
    label_width.grid(row=2, column=0, padx=10, pady=10)
    entry_width = ctk.CTkEntry(main_frame, width=150)
    entry_width.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    label_height = ctk.CTkLabel(main_frame, text="Nuevo Alto (opcional):")
    label_height.grid(row=3, column=0, padx=10, pady=10)
    entry_height = ctk.CTkEntry(main_frame, width=150)
    entry_height.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    sharpen_var = ctk.BooleanVar(value=False)
    check_sharpen = ctk.CTkCheckBox(main_frame, text="Aplicar nitidez", variable=sharpen_var)
    check_sharpen.grid(row=4, column=0, padx=10, pady=10)

    button_enhance = ctk.CTkButton(main_frame, text="Mejorar Imagen", command=enhance)
    button_enhance.grid(row=5, column=0, columnspan=3, pady=10)

    preview_label = ctk.CTkLabel(main_frame, text="Previsualización de la imagen", width=350, height=350)
    preview_label.grid(row=6, column=0, columnspan=3, pady=10)
