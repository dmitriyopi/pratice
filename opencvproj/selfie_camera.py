import cv2
import os
import time
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)
count = 0
photo_taken = False
timer_started = False
start_time = 0
cap = cv2.VideoCapture(0)
cooldown=2
dataset_path = "dataset/"
name = input("Введіть назву файлу: ")
save_path = os.path.join(dataset_path, name)
if not os.path.exists(save_path):
    os.makedirs(save_path)

def fingers_up(hand_landmarks):
    fingers_tips = [4, 8, 12, 16, 20]
    fingers = []
    for tip_id in fingers_tips:
        tip_id_y = hand_landmarks.landmark[tip_id].y
        dip_id_y = hand_landmarks.landmark[tip_id - 2].y
        fingers.append(tip_id_y < dip_id_y)
    return fingers

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_for_save = frame.copy()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    detected_five = False
    if result.multi_hand_landmarks:
        hand_landmark = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
        fingers = fingers_up(hand_landmark)
        total_fingers = fingers.count(True)
        if total_fingers == 5:
            detected_five = True
    if detected_five:
        if not timer_started:
            timer_started = True
            start_time = time.time()
            photo_taken = False
            print("Photo will taken at 5 sec")
    else:
        pass
    if timer_started:
        elapsed = time.time() - start_time
        remaining = max(0, int(5 - elapsed))
        cv2.putText(frame, f"Photo will taken at : {remaining} s", (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if elapsed >= 5 and not photo_taken:
            file_path = os.path.join(save_path, f"{count}.png")
            cv2.imwrite(file_path, frame_for_save)
            print(f"Збережено фото: {file_path}")
            count += 1
            photo_taken = True
            timer_started = False

    cv2.imshow("selfie camera", frame)
    key = cv2.waitKey(1)
    if key == 27 or count >= 5:
        break
cap.release()
cv2.destroyAllWindows()
