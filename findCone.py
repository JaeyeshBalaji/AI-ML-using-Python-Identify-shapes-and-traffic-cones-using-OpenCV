import cv2
import numpy as np

def empty(a):
    pass;

def stackImages(imgArray,scale,lables=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver


def getContours(img,img1):

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 500:
            cv2.drawContours(imgContour,cnt,-1,(143,0,255),3)
            peri= cv2.arcLength(cnt, True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            #print(approx)
            print(len(approx))
            objCor = len(approx)
            x,y,w,h = cv2.boundingRect(approx)
            #if objCor ==3: objectType = "Triangle"
            #elif objCor ==4:
             #   aspRatio = w/float(h)
              #  if aspRatio > 0.95 and aspRatio < 1.05 : objectType ="Square"
               # else: objectType ="Rectangle"
            #elif objCor == 5: objectType = "Pentagon"
            #elif objCor == 6: objectType = "Hexagon"
            #elif objCor == 10: objectType = "Star"
            #elif objCor == 8: objectType = "Circle"
            #else: objectType ="None"
            #imgContour = img.copy()
            cv2.rectangle(imgContour,(x-10,y-10),(x+w+10,y+h+10),(0,255,0),2)
            cv2.rectangle(img1,(x-10,y-10),(x+w+10,y+h+10),(0,255,0),2)


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)

cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",26,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",97,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",145,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

img = cv2.imread("Resources/cone.jpg")
imgResize = cv2.resize(img,(400,250))

while True:
    img = imgResize
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max","TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min","TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max","TrackBars")
    v_min = cv2.getTrackbarPos("Val Min","TrackBars")
    v_max = cv2.getTrackbarPos("Val Max","TrackBars")

    #print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask=cv2.inRange(imgHSV,lower,upper)

    imgResult = cv2.bitwise_and(img,img,mask=mask)

    imgContour = imgResult.copy()

    imgGray = cv2.cvtColor(imgContour, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)

    img1 = imgResize
    getContours(imgCanny,img1)
    #cv2.imshow("Contour Image", imgContour)
    #cv2.imshow("image Original", img)


    #cv2.imshow("image"()
    #cv2.imshow("image Original", img)
    #cv2.imshow("image HSV",imgHSV)
    #cv2.imshow("image mask", mask)
    #cv2.imshow("image Result", imgResult)
    imgStack = stackImages(([imgCanny,imgResult],[img,imgHSV]),0.6)
    cv2.imshow("image stack", imgStack)
    #cv2.imshow("Canny Image", imgCanny)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
