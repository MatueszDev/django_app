#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

def scanner(path):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    img = cv2.imread(path)
    height, width, channels = img.shape 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_gray  = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_gray = cv2.medianBlur(img_gray, 3)
    img_gray = Image.fromarray(img_gray)
    tmp = pytesseract.image_to_string(img_gray)
    return tmp

#    text_file = open("ocr/scripts/Output.txt", "w")
#    text_file.write("%s" % tmp)
#    text_file.close()
