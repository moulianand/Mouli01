from flask import Flask, request, jsonify
from PIL import Image
import pytesseract as pyt
import cv2
import numpy as np
import requests
from io import BytesIO

app = Flask(__name__)

# Set the path to the Tesseract binary in your system
pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def ocr_image(image_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()

        # Ensure the response content is a valid image
        image = Image.open(BytesIO(response.content))
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Use Tesseract to perform OCR on the image
        extracted_text_tamil = pyt.image_to_string(img_cv, lang="tam")

        # Print the extracted text to the console
        print(f"Extracted Text: {extracted_text_tamil}")
        return extracted_text_tamil

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving the image from the URL: {e}")
        return ""

    except Exception as e:
        print(f"Error processing the image: {e}")
        return ""

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Get the image URL from the request JSON data
        data = request.json
        image_url = data.get('image_url')

        if not image_url:
            return jsonify({"error": "Please provide the 'image_url' parameter in the request JSON."}), 400

        # Call the OCR function and store the result
        result = ocr_image(image_url)

        # Return the extracted text as JSON response
        return jsonify({"extracted_text": result})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
