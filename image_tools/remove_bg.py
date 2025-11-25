from rembg import remove
from PIL import Image

def remove_background(input_path, output_path):
    img = Image.open(input_path)
    result = remove(img)
    from PIL import Image as PILImage
    if not isinstance(result, PILImage.Image):
        result = PILImage.fromarray(result)
    result.save(output_path)
