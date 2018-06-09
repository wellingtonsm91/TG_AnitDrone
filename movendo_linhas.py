"""
Created on Fri Jun 01 18:43:24 2018

@author: wellington
"""

#import numpy as np

#Coloquei um comentário
import cv2

cap = cv2.VideoCapture(0)

i =0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    
    cv2.rectangle(gray,(i,i),(400,400),(250,250,250),5)
    cv2.imshow('frame',gray)
    
    i = i+1
    
    if i == 300:
        i = 0
        
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
        
