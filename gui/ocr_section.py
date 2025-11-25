import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from .utils import show_image_preview

def show_ocr_section(main_frame):
    def select_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.webp")])
        if file_path:
            entry_image_path.delete(0, ctk.END)
            entry_image_path.insert(0, file_path)
            show_image_preview(file_path, preview_label, size=(200, 200))

    def recognize_text():
        input_path = entry_image_path.get()
        if not input_path:
            messagebox.showerror("Error", "Selecciona una imagen")
            return
        try:
            import pytesseract
            import os
            tesseract_path = os.path.join(os.path.dirname(__file__), '..', 'tesseract', 'tesseract.exe')
            pytesseract.pytesseract.tesseract_cmd = os.path.abspath(tesseract_path)
            img = Image.open(input_path)
            text = pytesseract.image_to_string(img, lang="spa")
            text_box.configure(state="normal")
            text_box.delete("1.0", ctk.END)
            text_box.insert(ctk.END, text)
            text_box.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reconocer el texto: {e}\nAsegúrate que tesseract.exe está en la carpeta 'tesseract' dentro del proyecto.")

    label_image = ctk.CTkLabel(main_frame, text="Seleccionar Imagen:")
    label_image.grid(row=0, column=0, padx=10, pady=10)
    entry_image_path = ctk.CTkEntry(main_frame, width=500)
    entry_image_path.grid(row=0, column=1, padx=10, pady=10)
    button_search = ctk.CTkButton(main_frame, text="Buscar", command=select_image)
    button_search.grid(row=0, column=2, padx=10, pady=10)

    button_ocr = ctk.CTkButton(main_frame, text="Reconocer Texto", command=recognize_text)
    button_ocr.grid(row=1, column=0, columnspan=3, pady=10)

    preview_label = ctk.CTkLabel(main_frame, text="Previsualización de la imagen", width=350, height=200)
    preview_label.grid(row=2, column=0, columnspan=3, pady=10)

    text_box = ctk.CTkTextbox(main_frame, width=600, height=200)
    text_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    text_box.insert(ctk.END, "El texto reconocido aparecerá aquí...")
    text_box.configure(state="disabled")
