import pytesseract as pyt
import cv2


img = cv2.imread("tampic.jpg")
pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

extracted_text_tamil = pyt.image_to_string(img, lang="tam")

print(extracted_text_tamil)
