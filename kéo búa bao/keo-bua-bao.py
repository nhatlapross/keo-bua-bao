import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
 
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]

img_height = 330
img_width =187

randomNumber = 1
 
while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.94375, 0.94375)
    imgScaled = imgScaled[:, 75:470]

     # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:
        if stateResult is False:
            timer = time.time() - intialTime
            cv2.putText(imgBG,str(int(timer)),(740,225),cv2.FONT_HERSHEY_PLAIN,4,(255,0,255),4)
            if timer>3:
                stateResult = True
                timer = 0 

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png')
                    # imgBG = cvzone.overlayPNG(imgBG,imgAI,(432,80))
                    imgBG[ 81:81+img_height , 420:420+img_width ] = imgAI
                    
                    if (playerMove == 1 and randomNumber == 3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber == 2):
                        scores[1] +=1

                    if (playerMove == 3 and randomNumber == 1) or (playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber == 3):
                        scores[0] +=1

    a = 0
    imgBG[27+a:480-a,815+a:1210-a] = imgScaled

    if stateResult:
        imgAI = cv2.imread(f'Resources/{randomNumber}.png')
        # imgBG = cvzone.overlayPNG(imgBG,imgAI,(432,80))
        imgBG[ 81:81+img_height , 420:420+img_width ] = imgAI

    cv2.putText(imgBG,str(scores[0]),(520,460),cv2.FONT_HERSHEY_PLAIN,4,(255,0,255),4)
    cv2.putText(imgBG,str(scores[1]),(985,460),cv2.FONT_HERSHEY_PLAIN,4,(255,0,255),4)
           

    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled", imgScaled)
 
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False
    elif key == ord('q'):
        cv2.destroyAllWindows()
        cap.release()