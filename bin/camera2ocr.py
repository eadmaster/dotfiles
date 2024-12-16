#!/usr/bin/env python

# derived from https://github.com/maazismail/ocr-camera

import sys
import cv2
import pytesseract
import numpy as np

# TODO: support alternative OCR  https://github.com/mftnakrsu/Comparison-of-OCR
# TODO: use OpenCV’s EAST text detector for natural scenes https://pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
# TODO: add more options https://github.com/nathanaday/RealTime-OCR

cam = cv2.VideoCapture(0)
#cv2.namedWindow("OG")

USAGE_TEXT="press SPACEBAR for OCR, Esc to quit.\n"

osd_font = cv2.FONT_HERSHEY_COMPLEX
#tesseract_custom_config = r'--oem 3 --psm 6'
tesseract_custom_config = r'-l eng+ita+jpn'



def detect_and_draw_boxes(img):
    # https://nanonets.com/blog/ocr-with-tesseract/#gettingboxesaroundtext
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img, config=tesseract_custom_config) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
# end of detect_and_draw_boxes

def preprocess(img):
    # https://github.com/MauryaRitesh/OCR-Python/blob/master/OCR_Tesseract_Python.ipynb
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
# end of preprocess




while True:
    ret, frame = cam.read()
    #flip = cv2.flip(frame, 1)  #flipping camera to fix alignment    

    cv2.putText(frame, USAGE_TEXT,(0,100),osd_font,1,(255,255,255)) # ,3)  #text,coordinate,font,size of text,color,thickness of font
    cv2.imshow("OG", frame)

    k = cv2.waitKey(1)
    if k%256 == 32:
        #cv2.imwrite("capture.png", frame)
        #print("Printing...")
        #img = cv2.imread('capture.png')
        img = frame
        
        #cv2.putText(frame, "OCRing...",(0,100),osd_font,1,(255,255,255)) # ,3)  #text,coordinate,font,size of text,color,thickness of font
                
        preprocess(img)
        detect_and_draw_boxes(img)
        cv2.imshow("OG", frame)
        
        print(pytesseract.image_to_string(img, config=tesseract_custom_config))
        
        cv2.waitKey(0)
        # TODO: highlight text being read as rects

    elif k%256 == 27:
        print("Closing...")
        break
    
    #TODO: detect if the window was closed and terminate the loop  https://stackoverflow.com/questions/35003476/opencv-python-how-to-detect-if-a-window-is-closed
    #if (cv2.getWindowProperty('OG', 0) == -1):
    #if (cv2.getWindowProperty('OG', cv2.WND_PROP_AUTOSIZE) == -1):
    #if (cv2.getWindowProperty('OG', cv2.WND_PROP_AUTOSIZE) == -1):
    #    break
# end while

cam.release()
cv2.destroyAllWindows()