import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from image_tools.remove_bg import remove_background
from .utils import show_image_preview

def show_remove_bg_section(main_frame):
    def select_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.webp")])
        if file_path:
            entry_image_path.delete(0, ctk.END)
            entry_image_path.insert(0, file_path)
            show_image_preview(file_path, preview_label)

    from .utils import show_progress_bar, run_with_progress

    def remove_bg():
        import os
        input_path = entry_image_path.get()
        output_name = entry_output_name.get()
        if not input_path:
            messagebox.showerror("Error", "Selecciona una imagen")
            return
        # Si no se coloca nombre, usar el nombre original
        if not output_name:
            import ntpath
            base = ntpath.basename(input_path)
            output_name = os.path.splitext(base)[0]
        output_path = f"{output_name}_nofondo.png"
        # Validar si el archivo ya existe
        if os.path.exists(output_path):
            resp = messagebox.askyesno("Archivo existente", f"La imagen '{output_path}' ya existe. ¿Desea sobreescribirla?")
            if not resp:
                return
        def task():
            try:
                remove_background(input_path, output_path)
                messagebox.showinfo("Éxito", f"Imagen sin fondo guardada como {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo quitar el fondo: {e}")
        run_with_progress(task, progress_bar, progress_label, main_frame)

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

    button_remove_bg = ctk.CTkButton(main_frame, text="Quitar Fondo", command=remove_bg)
    button_remove_bg.grid(row=2, column=0, columnspan=3, pady=10)

    preview_label = ctk.CTkLabel(main_frame, text="Previsualización de la imagen", width=350, height=350)
    preview_label.grid(row=3, column=0, columnspan=3, pady=10)

    # Barra de progreso debajo de la previsualización
    progress_bar, progress_label = show_progress_bar(main_frame, row=4, columnspan=3)
