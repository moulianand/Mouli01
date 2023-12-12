from flask import Flask, request
from PIL import Image
import pytesseract as pyt
import cv2
import numpy as np
import requests
from io import BytesIO

app = Flask(__name__)

# Print the Tesseract path for debugging
print(f"Tesseract path: {pyt.pytesseract.tesseract_cmd}")

def ocr_image(image_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()

        # Ensure the response content is a valid image
        image = Image.open(BytesIO(response.content))
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Rest of your code...
        extracted_text_tamil = pyt.image_to_string(img_cv, lang="tam")
        return extracted_text_tamil

    except requests.exceptions.RequestException as e:
        return f"Error retrieving the image from the URL: {e}"

    except Exception as e:
        return f"Error processing the image: {e}"

@app.route('/')
def hello():
    image_url = request.args.get('image_url')
    if not image_url:
        return "Please provide the 'image_url' parameter in the URL."
    
    result = ocr_image(image_url)
    return f"Extracted Text: {result}"

if __name__ == '__main__':
    app.run(debug=True)


