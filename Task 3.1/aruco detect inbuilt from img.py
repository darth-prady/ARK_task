import cv2
import numpy as np

img=cv2.imread("detect aruco.jpg")
dict=cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
parameters=cv2.aruco.DetectorParameters_create()
cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
(corners,ids,rejected)=cv2.aruco.detectMarkers(img,dict,parameters=parameters)
    
if len(corners)>0:
    ids=ids.flatten()

    for (corner,id) in zip(corners,ids):
        corners=corner.reshape(4,2)
        (tl,tr,br,bl)=corners

        tr=(int(tr[0]),int(tr[1]))
        br=(int(br[0]),int(br[1]))
        tl=(int(tl[0]),int(tl[1]))
        bl=(int(bl[0]),int(bl[1]))

        cv2.line(img,tl,tr,(0,255,0),2)
        cv2.line(img,tr,br,(0,255,0),2)
        cv2.line(img,br,bl,(0,255,0),2)
        cv2.line(img,bl,tl,(0,255,0),2)
        
        cv2.putText(img, "id="+str(id),(tl[0], tl[1] - 15),cv2.FONT_HERSHEY_SIMPLEX,2.5, (0, 0, 0))

resized = np.full(((img.shape[0])//2,(img.shape[1])//2,3),255,dtype=np.uint8)

for i in range((img.shape[0])//2):
    for j in range((img.shape[1])//2):
        sum1,sum2,sum3=0,0,0
        for k in range(2):
            sum1+=img[i*2+k][j*2+k][0]
            sum2+=img[i*2+k][j*2+k][1]
            sum3+=img[i*2+k][j*2+k][2]
        resized[i][j][0]=sum1/2
        resized[i][j][1]=sum2/2
        resized[i][j][2]=sum3/2

cv2.imshow("aruco",resized)
cv2.waitKey(0)
cv2.destroyAllWindows()