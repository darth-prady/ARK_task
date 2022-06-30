import cv2
import numpy as np
from matplotlib import pyplot as plt

limg=cv2.imread("left.png",cv2.IMREAD_GRAYSCALE)
rimg=cv2.imread("right.png",cv2.IMREAD_GRAYSCALE)
obs=cv2.imread("bike.png",cv2.IMREAD_GRAYSCALE)

p_left = [[640.0,   0.0, 640.0, 2176.0], 
         [0.0, 480.0, 480.0,  552.0], 
         [0.0,   0.0,   1.0,    1.4]]
p_right = [[640.0,   0.0, 640.0, 2176.0], 
          [0.0, 480.0, 480.0,  792.0], 
          [0.0,   0.0,   1.0,    1.4]]

cv2.namedWindow("Left",cv2.WINDOW_NORMAL)
cv2.namedWindow("Right",cv2.WINDOW_NORMAL)

cv2.imshow("Left",limg)
cv2.imshow("Right",rimg)

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=13)
depthmap = stereo.compute(limg,rimg)

threshold = 0.999
res = cv2.matchTemplate(limg,obs,cv2.TM_CCOEFF_NORMED)
loc = np.where(res >= threshold)

if(len(loc[0]) != 0 and len(loc[1]) != 0):
    for pt in zip(*loc[::-1]):
        cv2.rectangle(limg, pt, (pt[0] + obs.shape[1], pt[1] + obs.shape[0]), (0,255,255), 3)
        cv2.imshow("temp",limg)
        x=pt[1] + obs.shape[0]//2
        y=pt[0] + obs.shape[1]//2

f=p_left[0][0]
d=p_right[1][3]-p_left[1][3]
dist=f*d/depthmap[x][y]
print("Distance = ",dist)

plt.title("Depth Map")
plt.imshow(depthmap)
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()