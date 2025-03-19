import cv2
import numpy as np

# Upload the images
img1 = cv2.imread('casita1.JPG')
img2 = cv2.imread('casita2.JPG')

""" # Resize the images (just in case)
h, w, _ = img1.shape
img1 = cv2.resize(img1, (h * 100, w * 100))
img2 = cv2.resize(img2, (h * 100, w * 100)) """

""" # Convert to grayscale (if the image is on color)
grayImg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
grayImg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) """

# Sobel in X
sobel_x1 = cv2.Sobel(img1, cv2.CV_64F, 1, 0, ksize=3)
sobel_x1 = cv2.convertScaleAbs(sobel_x1)

sobel_x2 = cv2.Sobel(img2, cv2.CV_64F, 1, 0, ksize=3)
sobel_x2 = cv2.convertScaleAbs(sobel_x2)

# Sobel in Y
sobel_y1 = cv2.Sobel(img1, cv2.CV_64F, 0, 1, ksize=3)
sobel_y1 = cv2.convertScaleAbs(sobel_y1)

sobel_y2 = cv2.Sobel(img2, cv2.CV_64F, 0, 1, ksize=3)
sobel_y2 = cv2.convertScaleAbs(sobel_y2)

sobel_combined1 = cv2.addWeighted(sobel_x1, 0.5, sobel_y1, 0.5, 0)
sobel_combined2 = cv2.addWeighted(sobel_x2, 0.5, sobel_y2, 0.5, 0)

# Show the differences between the images
diff = cv2.absdiff(sobel_combined1, sobel_combined2)

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('difference', diff)
cv2.waitKey(0)
cv2.destroyAllWindows()