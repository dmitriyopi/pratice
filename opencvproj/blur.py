import cv2,time
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

webcamera=cv2.VideoCapture(0)
while True:
    check,frame=webcamera.read()
    frame = cv2.flip(frame, 1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
    for x,y,w,h in face:
        face_roi=frame[y:y+h,x:x+w].copy()
        blurred_face = cv2.GaussianBlur(face_roi, (0, 0), sigmaX=15, sigmaY=15)
        frame[y:y+h,x:x+w]=blurred_face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

    cv2.imshow("Blurred Faces - Press Esc to Quit", frame)

    key = cv2.waitKey(10)
    if key==27:
        break
webcamera.release()
cv2.destroyAllWindows()