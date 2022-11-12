import cv2
import time
import numpy as np
import driver as hd
import math
import osascript


cap = cv2.VideoCapture(0)

previous_time = 0
detector = hd.handDetector(detectionCon=0.7)



while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue
    
    image = detector.findHands(cv2.flip(image, 0))
    land_mark_list = detector.findPosition(image, draw=False)

    if len(land_mark_list) != 0:
        if (len(detector.handType) > 1):
            continue
        if (len(detector.handType) == 1):
            if (detector.handType[0] == "Left"):
                x1, y1 = land_mark_list[4][1], land_mark_list[4][2]
                x2, y2 = land_mark_list[8][1], land_mark_list[8][2]
                x3, y3 = land_mark_list[12][1], land_mark_list[12][2]
                x4, y4 = land_mark_list[2][1], land_mark_list[2][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (x3, y3), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (x4, y4), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.line(image, (x3, y3), (x4, y4), (255, 0, 255), 3)
                cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                length = math.hypot(x2 - x1, y2 - y1)
                stop = math.hypot(x4 - x3, y4 - y3)
                # # Hand range 50 - 300
                # # Volume Range -65 - 0
                if (stop > 200):
                    vol = np.interp(length, [30,350], [0, 120])
                    osascript.osascript("set volume output volume {0}".format(vol))
                
            if (detector.handType[0] == "Right"):
                x1, y1 = land_mark_list[12][1], land_mark_list[12][2]
                x2, y2 = land_mark_list[0][1], land_mark_list[0][2]
                x3, y3 = land_mark_list[4][1], land_mark_list[4][2]
                x4, y4 = land_mark_list[20][1], land_mark_list[20][2]

                stop_right1 = math.hypot(x4 - x3, y4 - y3)
                stop_right2 = math.hypot(x2 - x1, y2 - y1)
                skip = math.hypot(x2 - x1, y2 - y1)
                print("log: {0}".format(stop_right1))
                print("log: {0}".format(stop_right2))
                if (stop_right1 < 250 and stop_right2 < 400):
                    osascript.osascript("""tell application "Spotify" to pause""")
                    time.sleep(1)
                elif (stop_right1 > 350 and stop_right2 > 450):
                    osascript.osascript("""tell application "Spotify" to play""")
                    time.sleep(1)
                elif (stop_right1 > 300 and stop_right1 <= 400 and stop_right2 < 300):
                    osascript.osascript("""tell application "Spotify" to next track""")
                    time.sleep(2)
                elif (stop_right1 > 400 and stop_right2 < 450):
                    osascript.osascript("""tell application "Spotify" to previous track""")
                    time.sleep(2)

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(image, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 108, 0), 2)
    cv2.imshow("image", cv2.flip(image, -1))
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()

