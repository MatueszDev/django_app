import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys


def scan_for_drawings(img):
    #handling too big resolutions
    height, width, channels = img.shape 
    if(height > 2500 or width > 2500):
        img = cv2.pyrDown(img) 
    #process image
    contours, hierarchy = get_areas(img)
    contours2, mask = get_text(img)
    centers = mark_text(img, contours2, mask)
    crops = get_drawings(img, contours, hierarchy, centers)
    #this is an option, but some data is lost (blurred image):
    #if(height > 2500 or width > 2500):
    #    img = cv2.pyrUp(img) 
    return img, crops

def mark_text(img, contours, mask):
    centers = list()
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, i, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
        if r > 0.2 and w > 8 and h > 8 and h < 100 and w > 200:  
            cv2.rectangle(img, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)
            cnt = contours[i]
            moments = cv2.moments(cnt)
            if(moments['m00']):
                center_x = int(moments['m10']/moments['m00'])
                center_y = int(moments['m01']/moments['m00'])
                cv2.circle(img, (center_x, center_y), 5, (255,0,0), thickness=5)
                centers.append((center_x, center_y))
            else:
                continue
    return centers

def get_drawings(img, contours, hierarchy, centers):
    crops = list()
    for c in zip(contours, hierarchy):
        rect = cv2.boundingRect(c[0])
        current_hierarchy = c[1]
        x,y,w,h = rect
        color = (0,0,255)
        if(current_hierarchy[3] < 0): 
            np.delete(contours, c[0])
            continue
        stop = 1
        if(h > 50):
            for center in centers:
            #False - checks if it is no not
            #if it is then 1, -1 if not and 0 if on border
                if(cv2.pointPolygonTest(c[0],center,False) == 1):
                    stop = 0
            if(stop):
                #draw rectangles (use for debugging)
                #cv2.rectangle(img, (x,y), (x+w, y+h), color, 5)
                crops.append(img[y:y+h, x:x+w])
    return crops

def get_text(img):
    #gradient method
    small = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)
    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #connecting
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1)) 
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    im2, contours2, hierarchy2 = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    mask = np.zeros(bw.shape, dtype=np.uint8)
    return contours2, mask

def get_areas(img):
    kernel = np.ones((20,20),np.uint8)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_gray = cv2.threshold(img_gray, 200, 255, 0)
    erosion = cv2.erode(img_gray,kernel, 2)
    im2, contours, hierarchy = cv2.findContours(erosion, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]
    return contours, hierarchy

if __name__ == "__main__":
    #uncomment line 61 for debugging
    image = cv2.imread(str(sys.argv[1]))
    image, crops = scan_for_drawings(image)
    for crop in crops:
        cv2.imshow("Show",crop)
        cv2.waitKey(30000)
        cv2.destroyAllWindows()
    cv2.imshow("Show", image)
    cv2.waitKey(30000)
    cv2.destroyAllWindows()
