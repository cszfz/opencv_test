#OpenCV-Python Tutorials Core Operations

import cv2


#Measuring Performance with OpenCV
e1 = cv2.getTickCount()
# your code execution
e2 = cv2.getTickCount()
time = (e2 - e1)/ cv2.getTickFrequency()

#You can do the same with time module. 
#Instead of cv2.getTickCount, use time.time() function. 
#Then take the difference of two times.


#Default Optimization in OpenCV
