from flask import Flask, request
from PIL import Image
import pytesseract as pyt
import cv2
import numpy as np
import requests
from io import BytesIO
from bs4 import BeautifulSoup

app = Flask(__name__)

def ocr_image(image_url, extract_data=False):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()
        
        image = Image.open(BytesIO(response.content))
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        extracted_text_tamil = pyt.image_to_string(img_cv, lang="tam")
        
        extracted_data = None
        if extract_data:
            soup = BeautifulSoup(response.content, 'html.parser')
            extracted_data = soup.get_text()
        
        return extracted_text_tamil, extracted_data
    
    except requests.exceptions.RequestException as e:
        return f"Error retrieving the image from the URL: {e}"
    except Exception as e:
        return f"Error processing the image: {e}"

@app.route('/')
def hello():
    extract_data = request.args.get('extract_data', 'false').lower() == 'true'
    image_url = request.args.get('image_url')
    
    if not image_url:
        return "Please provide the 'image_url' parameter in the URL."
    
    if extract_data:
        result_text, result_data = ocr_image(image_url, extract_data=True)
        return f"Extracted Text: {result_text}<br><br>Extracted Data: {result_data}"
    else:
        result_text = ocr_image(image_url)
        return f"Extracted Text: {result_text}"

if __name__ == '__main__':
    app.run(debug=True)

