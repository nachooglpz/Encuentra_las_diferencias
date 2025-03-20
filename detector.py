import cv2
import numpy as np
import imutils

# Upload the images
img1 = cv2.imread('adtime1.jpg')
img2 = cv2.imread('adtime2.jpg')

# Resize the images (just in case)
h, w, _ = img1.shape
res_ind = 1.1
img1 = cv2.resize(img1, (int(w/res_ind), int(h/res_ind)))
img2 = cv2.resize(img2, (int(w/res_ind), int(h/res_ind)))

# Convert to grayscale (if the image is on color)
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Sobel in X
sobel_x1 = cv2.Sobel(img1_gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_x1 = cv2.convertScaleAbs(sobel_x1)

sobel_x2 = cv2.Sobel(img2_gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_x2 = cv2.convertScaleAbs(sobel_x2)

# Sobel in Y
sobel_y1 = cv2.Sobel(img1_gray, cv2.CV_64F, 0, 1, ksize=3)
sobel_y1 = cv2.convertScaleAbs(sobel_y1)

sobel_y2 = cv2.Sobel(img2_gray, cv2.CV_64F, 0, 1, ksize=3)
sobel_y2 = cv2.convertScaleAbs(sobel_y2)

sobel_combined1 = cv2.addWeighted(sobel_x1, 0.5, sobel_y1, 0.5, 0)
sobel_combined2 = cv2.addWeighted(sobel_x2, 0.5, sobel_y2, 0.5, 0)

# Show the differences between the images
diff = cv2.absdiff(sobel_combined1, sobel_combined2)

# Apply a Threshold
# The function 'cv2.threshold()' returns a touple: (thresholded value, actual thresholded image)
_, thresholded = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY)

# Dilate the differences to find where to put the difference boxes
kernel = np.ones((5,5), np.int8)
dilated = cv2.dilate(thresholded, kernel)

# Designate the difference boxes contours
contours = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

# Calculate each box
for contour in contours:
    x, y, a, b = cv2.boundingRect(contour) # Calculate the points of the box
    # Draw the boxes in both images (just to know)
    cv2.rectangle(img1, (x, y), (x+a, y+b), (0, 0, 255), 2)
    cv2.rectangle(img2, (x, y), (x+a, y+b), (0, 0, 255), 2)
    
# Concatenating the images to show the results
result = np.hstack((img1, img2))

cv2.imshow('Spot the Differences Solved:', result)
cv2.waitKey()
cv2.destroyAllWindows()