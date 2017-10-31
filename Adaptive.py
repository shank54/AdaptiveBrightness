import cv2
import numpy as np
import wmi

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

brightness = 0 
c = wmi.WMI(namespace='wmi')
methods = c.WmiMonitorBrightnessMethods()[0]

cap = cv2.VideoCapture(0)

while True:
	ret, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray,1.3,5)

	# if face is detected then set the brightness to higher value
	if(len(faces)):
		brightness = 50
	# else set the brightness to lower value
	else:
		brightness = 0
	methods.WmiSetBrightness(brightness,0)

	for(x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) # draws a rectangle around the face
		roi_gray = gray[y:y+h,x:x+w]
		roi_color = img[y:y+h,x:x+w]
		cv2.imshow('img',img) #opens a new window and displays the image captured by camera
		k = cv2.waitKey(30) & 0xff
		if k == 27:# Reset the brightness to 0 when Esc is pressed and close all windows
			brightness = 0
			methods.WmiSetBrightness(brightness,0)
			cap.release()
			cv2.destroyAllWindows()