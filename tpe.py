import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

# Create the trackbars window
trackbars = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow("trackbars")

hlt = "Hue Low"
hht = "Hue High"
slt = "Saturation Low"
sht = "Saturation High"
vlt = "Value Low"
vht = "Value High"

# Create trackbars
cv2.createTrackbar(hlt, "trackbars", 0, 179, nothing)
cv2.createTrackbar(hht, "trackbars", 0, 179, nothing)
cv2.createTrackbar(slt, "trackbars", 0, 255, nothing)
cv2.createTrackbar(sht, "trackbars", 0, 255, nothing)
cv2.createTrackbar(vlt, "trackbars", 0, 255, nothing)
cv2.createTrackbar(vht, "trackbars", 0, 255, nothing)

def setTb(hl, hh, sl, sh, vl, vh):
    cv2.setTrackbarPos(hlt, "trackbars", hl)
    cv2.setTrackbarPos(hht, "trackbars", hh)
    cv2.setTrackbarPos(slt, "trackbars", sl)
    cv2.setTrackbarPos(sht, "trackbars", sh)
    cv2.setTrackbarPos(vlt, "trackbars", vl)
    cv2.setTrackbarPos(vht, "trackbars", vh)


# Setting hh, sh, vh to track everything on the screen
setTb(0, 179, 0, 255, 0, 255)

while True:
    ret, frame = cap.read()

    # Blur the image
    blur = cv2.GaussianBlur(frame, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get trackbars value to define hsvMin and hsvMax
    hLow = cv2.getTrackbarPos(hlt, "trackbars")
    hHigh = cv2.getTrackbarPos(hht, "trackbars")
    sLow = cv2.getTrackbarPos(slt, "trackbars")
    sHigh = cv2.getTrackbarPos(sht, "trackbars")
    vLow = cv2.getTrackbarPos(vlt, "trackbars")
    vHigh = cv2.getTrackbarPos(vht, "trackbars")

    # lower and upper range to track
    hsvMin = np.array([hLow,sLow,vLow])
    hsvMax = np.array([hHigh,sHigh,vHigh])

    mask = cv2.inRange(hsv,hsvMin, hsvMax)
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    result = cv2.bitwise_and(frame,frame, mask = bmask)

    # -- CONTOURS --
    ret, thresh = cv2.threshold(bmask, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, 1, 2)

    if len(contours) > 0:       # Prevent from error
        cnt = contours[-1]
        x,y,w,h = cv2.boundingRect(cnt)  #IndexError: list index out of range
        if w > 40 and h > 40:
            print x,y,w,h
            cv2.rectangle(result,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.circle(result, (x+w/2,y+h/2), 2, (0,0,255), 2)


    # Display every windows
    cv2.imshow("original", frame)
    cv2.imshow("trackbars", trackbars)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    # Keyboard inputs
    k = cv2.waitKey(1) & 0xFF
    if k == 27:             # Press ESC key to quit
        break
    elif k == ord('b'):     # Shortcut to track my blue handspinner :D
        setTb(106, 179, 98, 174, 37, 200)

    elif k == ord('r'):     # Shortcut to reset trackbars
        setTb(0, 179, 0, 255, 0, 255)

cap.release()
cv2.destroyAllWindows()
