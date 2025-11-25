import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()
from image_tools.tools import convert_image_file
from .utils import show_image_preview

def show_convert_section(main_frame):
    def select_images():
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.webp;*.heic")])
        if file_paths:
            entry_image_path.delete(0, ctk.END)
            entry_image_path.insert(0, "; ".join(file_paths))
            # Mostrar la previsualización de la primera imagen seleccionada
            show_image_preview(file_paths[0], preview_label)

    from .utils import show_progress_bar

    def convert_images():
        import os
        import threading
        import datetime
        input_paths = entry_image_path.get().split('; ')
        output_name = entry_output_name.get()
        selected_format = format_var.get()
        if not input_paths or not selected_format or input_paths == ['']:
            messagebox.showerror("Error", "Selecciona una o más imágenes y formato")
            return

        # Carpeta base: donde está el .exe si está congelado, o el script si no
        import sys
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "Images Converted")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        # Subcarpeta por fecha
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        date_dir = os.path.join(images_dir, today)
        if not os.path.exists(date_dir):
            os.makedirs(date_dir)

        # Subir el frame de progreso justo debajo de la previsualización
        progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        progress_frame.grid(row=5, column=0, columnspan=3, pady=(1, 1), sticky="ew")
        progress_frame.columnconfigure(0, weight=1)
        # Preloader arriba del texto
        preloader = ctk.CTkLabel(progress_frame, text="⏳", font=("Arial", 32), anchor="center")
        preloader.grid(row=0, column=0, pady=(0, 1))
        progress_label = ctk.CTkLabel(progress_frame, text="", width=200, anchor="center")
        progress_label.grid(row=1, column=0, pady=(0, 1))
        progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
        progress_bar.grid(row=2, column=0, pady=(0, 1))
        progress_bar.set(0)

        def task():
            import ntpath
            import time
            successes = 0
            errors = []
            total = len(input_paths)
            for idx, path in enumerate(input_paths):
                def update_ui():
                    progress_text = f"Procesando {idx+1}/{total} imágenes"
                    progress_label.configure(text=progress_text)
                    progress_bar.set(0)
                    show_image_preview(path, preview_label)
                main_frame.after(0, update_ui)

                # Simular progreso individual de la imagen
                for p in range(1, 101, 5):
                    main_frame.after(0, lambda val=p: progress_bar.set(val/100))
                    time.sleep(0.01)

                if not os.path.exists(path):
                    errors.append(f"No existe: {path}")
                    continue
                if output_name:
                    name = output_name if idx == 0 else f"{output_name}-{idx}"
                else:
                    name = os.path.splitext(ntpath.basename(path))[0]
                output_path = os.path.join(date_dir, f"{name}.{selected_format}")
                if os.path.exists(output_path):
                    result = []
                    def ask_overwrite():
                        resp = messagebox.askyesno("Archivo existente", f"La imagen '{output_path}' ya existe. ¿Desea sobreescribirla?")
                        result.append(resp)
                    main_frame.after(0, ask_overwrite)
                    while not result:
                        time.sleep(0.05)
                    if not result[0]:
                        continue
                try:
                    convert_image_file(path, output_path[:-len(f'.{selected_format}')], selected_format)
                    main_frame.after(0, lambda: progress_bar.set(1))
                    successes += 1
                except Exception as e:
                    errors.append(f"{path}: {e}")
                time.sleep(0.1)
            def finish_ui():
                progress_label.configure(text="Listo")
                progress_bar.set(1)
                preloader.configure(text="✔️")
                if successes:
                    messagebox.showinfo("Éxito", f"{successes} imagen(es) convertida(s) correctamente.")
                if errors:
                    messagebox.showerror("Errores", "\n".join(errors))
                import time
                time.sleep(1)
                progress_frame.destroy()
            main_frame.after(0, finish_ui)
        threading.Thread(target=task).start()

    label_image = ctk.CTkLabel(main_frame, text="Seleccionar Imagen:")
    label_image.grid(row=0, column=0, padx=10, pady=10)
    entry_image_path = ctk.CTkEntry(main_frame, width=500)
    entry_image_path.grid(row=0, column=1, padx=10, pady=10)
    button_search = ctk.CTkButton(main_frame, text="Buscar", command=select_images)
    button_search.grid(row=0, column=2, padx=10, pady=10)

    label_output = ctk.CTkLabel(main_frame, text="Nombre de la Imagen Nueva:")
    label_output.grid(row=1, column=0, padx=10, pady=10)
    entry_output_name = ctk.CTkEntry(main_frame, width=500)
    entry_output_name.grid(row=1, column=1, padx=10, pady=10)

    label_format = ctk.CTkLabel(main_frame, text="Formato de Conversión:")
    label_format.grid(row=2, column=0, padx=10, pady=10)
    formats = ["png", "jpg", "jpeg", "webp", "bmp", "tiff"]
    format_var = ctk.StringVar(value="png")
    option_menu = ctk.CTkOptionMenu(main_frame, variable=format_var, values=formats, width=250)
    option_menu.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky="ew")

    button_convert = ctk.CTkButton(main_frame, text="Convertir", command=convert_images)
    button_convert.grid(row=3, column=0, columnspan=3, pady=1)

    preview_label = ctk.CTkLabel(main_frame, text="Previsualización de la imagen", width=350, height=350)
    preview_label.grid(row=4, column=0, columnspan=3, pady=1)

    # (La barra de progreso y el texto se crean dinámicamente al convertir)
