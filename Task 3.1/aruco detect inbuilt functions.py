import cv2
import numpy as np

vid=cv2.VideoCapture(0,cv2.CAP_V4L2)
while True:
    isTrue,img=vid.read()

    if cv2.waitKey(10) & 0xFF==ord(' '):
        vid.release()
        break
    
    dict=cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters=cv2.aruco.DetectorParameters_create()

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

            cv2.putText(img, "ID = " + str(id),(tl[0], tl[1] - 15),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0))

    cv2.imshow("aruco",img)

cv2.destroyAllWindows()