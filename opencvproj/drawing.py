import cv2
import mediapipe as mp
from collections import deque
import numpy as np

black_points=[deque(maxlen=1024)]
yellow_points=[deque(maxlen=1024)]
green_points=[deque(maxlen=1024)]
purple_points=[deque(maxlen=1024)]
black_index=0
yellow_index=0
green_index=0
purple_index=0
kernel=np.ones((5,5),np.uint8)
colorIndex=0

colors = [(0, 0, 0), (0, 255, 255), (0, 255, 0), (255, 0, 255)]
paint=np.ones((471,636,3), dtype=np.uint8) * 255
paint=cv2.rectangle(paint,(40,1), (140,65), (0,0,0), 2)
paint=cv2.rectangle(paint,(160,1), (255,65), (0,0,0), 2)
paint=cv2.rectangle(paint,(275,1), (370,65), (0,255,255), 2)
paint=cv2.rectangle(paint,(390,1), (485,65), (0,255,0), 2)
paint=cv2.rectangle(paint,(505,1), (600,65), (255,0,255), 2)

cv2.putText(paint, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
cv2.putText(paint, "BLACK", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
cv2.putText(paint, "YELLOW", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)
cv2.putText(paint, "GREEN", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
cv2.putText(paint, "PURPLE", (515, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 2)
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.6)
mp_draw=mp.solutions.drawing_utils
cap=cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.rectangle(frame, (40,1), (140,65), (0,0,0), 2)
    frame = cv2.rectangle(frame, (160,1), (255,65), (0,0,0), 2)
    frame = cv2.rectangle(frame, (275,1), (370,65), (0,255,255), 2)
    frame = cv2.rectangle(frame, (390,1), (485,65), (0,255,0), 2)
    frame = cv2.rectangle(frame, (505,1), (600,65), (255,0,255), 2)
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(frame, "BLACK", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(frame, "YELLOW", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)
    cv2.putText(frame, "GREEN", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    cv2.putText(frame, "PURPLE", (515, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 2)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        landmarks = []
        for handlm in result.multi_hand_landmarks:
            for lm in handlm.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)
                landmarks.append([lmx, lmy])
            mp_draw.draw_landmarks(frame, handlm, mp_hands.HAND_CONNECTIONS)
        fore_finger = (landmarks[8][0], landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])
        cv2.circle(frame, center, 3, (0,255,0), -1)
        if (thumb[1] - center[1]) < 40:
            if center[1] <= 65:
                if 40 <= center[0] <= 140:
                    black_points = [deque(maxlen=1024)]
                    yellow_points = [deque(maxlen=1024)]
                    green_points = [deque(maxlen=1024)]
                    purple_points = [deque(maxlen=1024)]
                    black_index = yellow_index = green_index = purple_index = 0
                    paint[67:,:,:] = 255
                elif 160 <= center[0] <= 255:
                    colorIndex = 0
                elif 275 <= center[0] <= 370:
                    colorIndex = 1
                elif 390 <= center[0] <= 485:
                    colorIndex = 2
                elif 505 <= center[0] <= 600:
                    colorIndex = 3
            else:
                if colorIndex == 0:
                    black_points[black_index].appendleft(center)
                elif colorIndex == 1:
                    yellow_points[yellow_index].appendleft(center)
                elif colorIndex == 2:
                    green_points[green_index].appendleft(center)
                elif colorIndex == 3:
                    purple_points[purple_index].appendleft(center)
        else:
            black_points.append(deque(maxlen=1024))
            yellow_points.append(deque(maxlen=1024))
            green_points.append(deque(maxlen=1024))
            purple_points.append(deque(maxlen=1024))
            black_index += 1
            yellow_index += 1
            green_index += 1
            purple_index += 1
    else:
        black_points.append(deque(maxlen=1024))
        yellow_points.append(deque(maxlen=1024))
        green_points.append(deque(maxlen=1024))
        purple_points.append(deque(maxlen=1024))
        black_index += 1
        yellow_index += 1
        green_index += 1
        purple_index += 1
    points = [black_points, yellow_points, green_points, purple_points]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k-1], points[i][j][k], colors[i], 2)
                cv2.line(paint, points[i][j][k-1], points[i][j][k], colors[i], 2)
    cv2.imshow("frame", frame)
    cv2.imshow("paint", paint)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()