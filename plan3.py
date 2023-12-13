from PIL import Image
import pytesseract as pyt
import cv2
import numpy as np
import requests
from io import BytesIO

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

if __name__ == '__main__':
    # Replace the placeholder URL with the actual image URL
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/%E0%AE%9A%E0%AE%A8%E0%AF%8D%E0%AE%A4%E0%AE%BF%E0%AE%AA%E0%AF%8D%E0%AE%AA%E0%AF%81%2C_%E0%AE%A4%E0%AF%8A._%E0%AE%AE%E0%AF%81._%E0%AE%9A%E0%AE%BF._%E0%AE%B0%E0%AE%95%E0%AF%81%E0%AE%A8%E0%AE%BE%E0%AE%A4%E0%AE%A9%E0%AF%8D.pdf/page18-1034px-%E0%AE%9A%E0%AE%A8%E0%AF%8D%E0%AE%A4%E0%AE%BF%E0%AE%AA%E0%AF%8D%E0%AE%AA%E0%AF%81%2C_%E0%AE%A4%E0%AF%8A._%E0%AE%AE%E0%AF%81._%E0%AE%9A%E0%AE%BF._%E0%AE%B0%E0%AE%95%E0%AF%81%E0%AE%A8%E0%AE%BE%E0%AE%A4%E0%AE%A9%E0%AF%8D.pdf.jpg"
    
    # Call the OCR function and store the result
    result = ocr_image(image_url)

    # The extracted text is also available in the 'result' variable if needed for further processing
