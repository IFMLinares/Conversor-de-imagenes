import customtkinter as ctk

def run_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("Herramientas de Imágenes")
    app.geometry("1050x600")
    app.minsize(900, 625)

    # Frame principal con menú lateral
    # Colores personalizados
    dark_sidebar = "#18191A"  # negro oscuro
    dark_bg = "#23272A"       # negro más claro
    light_sidebar = "#D4D4D4" # gris claro
    light_bg = "#F0F0F0"      # blanco no brillante


    sidebar = ctk.CTkFrame(app, width=180, height=600, fg_color=dark_sidebar)
    sidebar.grid(row=0, column=0, rowspan=2, sticky="nswe")
    sidebar.grid_propagate(False)

    # Título en el menú lateral (centrado, multilinea si es necesario)
    sidebar_title = ctk.CTkLabel(
        sidebar,
        text="Herramientas\nde Imágenes",  # Forzar salto de línea manual
        font=("Arial", 16, "bold"),
        text_color="#F0F0F0",
        justify="center",
        anchor="center",
        width=160,
        height=50
    )
    sidebar_title.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="nwe")

    main_frame = ctk.CTkFrame(app, fg_color=dark_bg)
    main_frame.grid(row=0, column=1, sticky="nsew")
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    # Importar las secciones modularizadas
    from gui.convert_section import show_convert_section
    from gui.remove_bg_section import show_remove_bg_section
    from gui.enhance_section import show_enhance_section
    from gui.ocr_section import show_ocr_section

    # Función para mostrar la sección seleccionada
    def show_section(section):
        for widget in main_frame.winfo_children():
            widget.destroy()
        if section == "convert":
            show_convert_section(main_frame)
        elif section == "remove_bg":
            show_remove_bg_section(main_frame)
        elif section == "enhance":
            show_enhance_section(main_frame)
        elif section == "ocr":
            show_ocr_section(main_frame)

    # Botones del menú lateral
    convert_btn = ctk.CTkButton(sidebar, text="Conversor de Imágenes", command=lambda: show_section("convert"), width=160)
    convert_btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    remove_bg_btn = ctk.CTkButton(sidebar, text="Remover Fondo", command=lambda: show_section("remove_bg"), width=160)
    remove_bg_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    enhance_btn = ctk.CTkButton(sidebar, text="Mejorar Calidad", command=lambda: show_section("enhance"), width=160)
    enhance_btn.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
    ocr_btn = ctk.CTkButton(sidebar, text="Reconocer Texto", command=lambda: show_section("ocr"), width=160)
    ocr_btn.grid(row=4, column=0, padx=10, pady=10, sticky="ew")


    # Switch de tema en la parte inferior izquierda
    def switch_theme():
        if theme_switch.get():
            ctk.set_appearance_mode("dark")
            theme_switch.configure(text="Tema oscuro")
            sidebar.configure(fg_color=dark_sidebar)
            main_frame.configure(fg_color=dark_bg)
            sidebar_title.configure(text_color="#F0F0F0")
        else:
            ctk.set_appearance_mode("light")
            theme_switch.configure(text="Tema claro")
            sidebar.configure(fg_color=light_sidebar)
            main_frame.configure(fg_color=light_bg)
            sidebar_title.configure(text_color="#18191A")

    theme_switch = ctk.CTkSwitch(sidebar, text="Tema oscuro", command=switch_theme, width=120)
    theme_switch.select()  # Activado por defecto (tema oscuro)
    sidebar.grid_rowconfigure(99, weight=1)  # Empuja el switch hacia abajo
    theme_switch.grid(row=99, column=0, padx=20, pady=20, sticky="sw")

    show_section("convert")

    app.mainloop()
