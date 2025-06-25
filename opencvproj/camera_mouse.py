import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
smoothening = 7
prev_x, prev_y = 0, 0
prev_index_y = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb)
    hands = output.multi_hand_landmarks

    index_x = index_y = thumb_x = thumb_y = 0


    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                if id == 4:
                    cv2.circle(frame, (x, y), 10, (0, 0, 255), cv2.FILLED)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

            curr_x = prev_x + (index_x - prev_x) / smoothening
            curr_y = prev_y + (index_y - prev_y) / smoothening
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y


            if abs(index_x - thumb_x) < 30 and abs(index_y - thumb_y) < 30:
                pyautogui.click()
                time.sleep(1)

    cv2.imshow("Mouse Control", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
