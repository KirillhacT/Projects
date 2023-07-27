from PIL import Image
import pytesseract
import os

def getPhotoToText():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    arr = os.listdir("images")
    image_path = f"images/{arr[0]}"
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image, lang="rus")
    return text