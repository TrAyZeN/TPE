import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

# Create the trackbars window
trackbars = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow("trackbars")

hl = "Hue Low"
hh = "Hue High"
sl = "Saturation Low"
sh = "Saturation High"
vl = "Value Low"
vh = "Value High"

# Create trackbars
cv2.createTrackbar(hl, "trackbars", 0, 179, nothing)
cv2.createTrackbar(hh, "trackbars", 0, 179, nothing)
cv2.createTrackbar(sl, "trackbars", 0, 255, nothing)
cv2.createTrackbar(sh, "trackbars", 0, 255, nothing)
cv2.createTrackbar(vl, "trackbars", 0, 255, nothing)
cv2.createTrackbar(vh, "trackbars", 0, 255, nothing)

# Setting hh, sh, vh to track everything on the screen
cv2.setTrackbarPos(hh, "trackbars", 179)
cv2.setTrackbarPos(sh, "trackbars", 255)
cv2.setTrackbarPos(vh, "trackbars", 255)

while True:
    ret, frame = cap.read()

    # Blur the image
    blur = cv2.GaussianBlur(frame, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get trackbars value to define hsvMin and hsvMax
    hLow = cv2.getTrackbarPos(hl, "trackbars")
    hHigh = cv2.getTrackbarPos(hh, "trackbars")
    sLow = cv2.getTrackbarPos(sl, "trackbars")
    sHigh = cv2.getTrackbarPos(sh, "trackbars")
    vLow = cv2.getTrackbarPos(vl, "trackbars")
    vHigh = cv2.getTrackbarPos(vh, "trackbars")

    # lower and upper range to track
    hsvMin = np.array([hLow,sLow,vLow])
    hsvMax = np.array([hHigh,sHigh,vHigh])

    mask = cv2.inRange(hsv,hsvMin, hsvMax)
    result = cv2.bitwise_and(frame,frame, mask = mask)

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
        cv2.setTrackbarPos(hl, "trackbars", 106)
        cv2.setTrackbarPos(hh, "trackbars", 179)
        cv2.setTrackbarPos(sl, "trackbars", 98)
        cv2.setTrackbarPos(sh, "trackbars", 174)
        cv2.setTrackbarPos(vl, "trackbars", 37)
        cv2.setTrackbarPos(vh, "trackbars", 200)

cap.release()
cv2.destroyAllWindows()
