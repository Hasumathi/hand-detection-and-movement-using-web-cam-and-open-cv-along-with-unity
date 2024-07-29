import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

width, height = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, height)
cap.set(4, width)

detector = HandDetector(maxHands=1, detectionCon=0.8)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAdd = ("127.0.0.1", 5054)

while True:
    success, img=cap.read()
    hands, img = detector.findHands(img)

    data = []
    if hands:
        hand = hands[0]
        lmList=hand['lmList']
        #print(lmList)
        for lm in lmList:
            data.extend([lm[0], height-lm[1],lm[2]])
        #print(data)
        sock.sendto(str.encode(str(data)), serverAdd)
    img = cv2.resize(img, (0,0), None, 0.5, 0.5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)