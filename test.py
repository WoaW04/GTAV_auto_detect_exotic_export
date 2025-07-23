import cv2
import numpy as np
import pygetwindow as gw
import pyautogui as pg

#t = gw.getAllTitles()
#print(t)
window = gw.getWindowsWithTitle("Grand Theft Auto V")
wd = window[0]
pg.screenshot(imageFilename="screen.png",region=(wd.left,wd.top,wd.width,wd.height))
img = cv2.imread("screen.png")
x,y,w,h=80,830,280,180
roi = img[y:y+h,x:x+w]
hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

lower_blue=np.array([100,100,200])
upper_blue=np.array([120,255,255])

msk = cv2.inRange(hsv_roi,lower_blue,upper_blue)
if cv2.countNonZero(msk)>0:
    print("exist")
else:
    print("no")

cv2.imshow('ROI',roi)
cv2.imshow('Mask',msk)
cv2.waitKey(0)
cv2.destroyAllWindows()
