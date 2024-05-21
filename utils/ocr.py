import io
import pytesseract
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_text_from_image(image:bytes):

    img = Image.open(io.BytesIO(image))
    return pytesseract.image_to_string(img)

if __name__ == "__main__":
    with open("image.png", "rb") as image_file:
        image = image_file.read()
    print(get_text_from_image(image))

