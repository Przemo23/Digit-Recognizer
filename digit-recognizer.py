import getopt
import os
import sys
import platform

import cv2
import pytesseract
from PIL import EpsImagePlugin
from PIL import Image

from config import gs_path, pytesseract_path
from helpers import delete_child_contours
from helpers import switch_letters_to_numbers

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = pytesseract_path
    EpsImagePlugin.gs_windows_binary = gs_path

# Process the commandline arguments
if len(sys.argv) < 2:
    print('Not enough arguments. Please insert the image path.')
    sys.exit(2)

i_image_path = ''
o_image_path = ''
PLAIN_DIGITS = True
OUTPUT = False
#Loading cmd-line params
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:p")
except getopt.GetoptError:
    print('Arguments Error: Failure while loading arguments')
    sys.exit(2)
for opt, arg in opts:
    if opt in ['-p']:
        PLAIN_DIGITS = False
    elif opt in ['-i']:
        i_image_path = arg
    elif opt in ['-o']:
        o_image_path = arg
        OUTPUT = True

# Converting the image to PNG
try:
    img_eps = Image.open(i_image_path)
    fig = img_eps.convert('RGBA')
except IOError:
    print('IO Error: The file cannot be found or the cannot be opened.')
    sys.exit(2)
image_png = 'tmp_convert_file.png'
img = fig.save(image_png, lossless=True)

# Loading the converted file
img = cv2.imread('tmp_convert_file.png')
os.remove('tmp_convert_file.png')

original_img = img.copy()
# Change the image to grayscale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Upscale the image if it is very small
if img.size < 100000:
    scale = 100000 / img.size
    img = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))
    original_img = cv2.resize(img, (
        int(img.shape[1] * scale), int(img.shape[0] * scale)))  # upscale the color version as well

# Apply GaussianBlur and thresholding for easier contour finding and better Tesseract performance
img = cv2.GaussianBlur(img, (5, 5), 0)
ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
thresh = img.copy()

rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
img = cv2.dilate(img, rect_kern, iterations=1)

# Find the contours
contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

# Remove contours within other contours
if PLAIN_DIGITS:
    hierarchy = hierarchy.tolist()[0]
    contours = delete_child_contours(contours, hierarchy)

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    # Skip extremely small contours
    if h * w < 200:
        continue
    # Draw the contour rectangle on the
    rect = cv2.rectangle(original_img, (x, y), (x + w, y + h), (255, 0, 255), 2)

    # Get the contour area, reverse Grayscale and apply addition Blur for better Tesseract performance
    digit_rect = thresh[y - 5:y + h + 5, x - 5:x + w + 5]
    digit_rect = cv2.bitwise_not(digit_rect)
    digit_rect = cv2.medianBlur(digit_rect, 5)

    # Recognize the digit in each contour and then
    digit_string = pytesseract.image_to_string(digit_rect, config='--oem 3 --psm 13')
    if PLAIN_DIGITS:
        digit_string = switch_letters_to_numbers(digit_string)
    digit = ''.join(e for e in digit_string if e.isdigit())

    cv2.putText(original_img, digit, (x + 1, y + 1), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(255, 0, 255),
                thickness=2)
if OUTPUT:
    cv2.imwrite(o_image_path,original_img)
cv2.imshow('borders', original_img)
cv2.waitKey(0)

