import cv2
webcamera = cv2.VideoCapture(0)
first_frame = None
while True:
    check, frame = webcamera.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if first_frame is None:
        first_frame = gray
        continue
    delta_frame_var = cv2.absdiff(first_frame, gray)
    threshold_frame = cv2.threshold(delta_frame_var, 50, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)
    contours,_ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Motion ", frame)

    key = cv2.waitKey(10)
    if key == 27:
        break

webcamera.release()
cv2.destroyAllWindows()
