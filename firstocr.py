from PIL import Image
import pytesseract

text = pytesseract.image_to_string(Image.open("q7.jpg"))

print(text)