import cv2
import numpy as np
import mediapipe as mp
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageSequence
Tk().withdraw()
is_gif = False
gif_frames = []
gif_index = 0
bg_path = askopenfilename(title="Оберіть зображення фону",filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
if not bg_path:
    print("Фон не вибрано,за замовчуванням чорний")
    background = np.zeros((480, 640, 3), dtype=np.uint8)
else:
    if bg_path.endswith('.gif'):
        is_gif=True
        gif=Image.open(bg_path)
        for frame in ImageSequence.Iterator(gif):
            frame=frame.convert('RGB')
            frame=frame.resize((640,480))
            frame=np.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            gif_frames.append(frame)
    else:
        background=cv2.imread(bg_path)
        background = cv2.resize(background, (640, 480))

mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()


    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = selfie_segmentation.process(rgb)
    mask = results.segmentation_mask
    condition = np.stack((mask,) * 3, axis=-1) > 0.6
    if is_gif:
        background=gif_frames[gif_index]
        gif_index=(gif_index+1)%len(gif_frames)
    output_img = np.where(condition, frame, background)
    cv2.imshow('background', output_img)
    key = cv2.waitKey(10)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
