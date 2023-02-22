import cv2
import random
import numpy as np

image = cv2.imread('sheets03.jpg')
blur = cv2.GaussianBlur(image, (1, 1), 0)
edges = cv2.Canny(blur, 50, 150, apertureSize=3)
cv2.imwrite('edges-50-150.jpg', edges)
minLineLength = 1000
lines = cv2.HoughLinesP(image=edges, rho=3, theta=np.pi / 90, threshold=480, lines=np.array([]),
                        minLineLength=minLineLength, maxLineGap=150)

a, b, c = lines.shape
for i in range(a):
    # print("Line " + str(i))
    # print(lines[i][0][0])
    # print(lines[i][0][1])
    # print(lines[i][0][2])
    # print(lines[i][0][3])

    cv2.line(image, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]),
             (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5)
    cv2.imwrite('houghlines5.jpg', image)
