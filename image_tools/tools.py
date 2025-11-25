from PIL import Image
from PIL import ImageFilter

def convert_image_file(input_path, output_name, selected_format):
    img = Image.open(input_path)
    output_path = f"{output_name}.{selected_format}"
    img.save(output_path)
    return output_path

def enhance_image(input_path, output_path, width=None, height=None, sharpen=False):
    img = Image.open(input_path)
    # Redimensionar si se especifica
    if width and height:
        img = img.resize((width, height), Image.LANCZOS)
    # Aplicar nitidez si se solicita
    if sharpen:
        img = img.filter(ImageFilter.SHARPEN)
    img.save(output_path)
    return output_path
