import io
import pytesseract
from PIL import Image

import dotenv
dotenv.load_dotenv()
import replicate

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

TEMPLATE = """
<|im_start|>system
You are a helpful assistant programmed to help with any prompt given. For every chunk of text you receive, you're tasked with providing a response based on the instructions provided (if any) .

Make sure to provide a clear and concise response to the user's prompt. Format your response in a way that emulates a Streamlit Markdown format.
<|im_end|>

<|im_start|>user
{prompt}<|im_end|>

<|im_start|>assistant
"""

def get_text_from_image(image:bytes):

    img = Image.open(io.BytesIO(image))
    return pytesseract.image_to_string(img)

def get_help_from_arctic(image_text, instructions):

    input = {
        "top_k": 50,
        "top_p": 0.9,
        "prompt": f"Prompt: {image_text}\nInstructions: {instructions}",
        "temperature": 0.2,
        "max_new_tokens": 512,
        "min_new_tokens": 0,
        "stop_sequences": "<|im_end|>",
        "prompt_template": TEMPLATE,
        "presence_penalty": 1.15,
        "frequency_penalty": 0.2
        }    

    response = []

    for event in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input=input
    ):
        response.append(str(event))

    return "".join(response)

if __name__ == "__main__":
    with open("image-2.png", "rb") as image_file:
        image = image_file.read()
    print(get_help_from_arctic(get_text_from_image(image)))

