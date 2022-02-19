
import numpy as np
import telegram_send
import cv2,time
from datetime  import datetime
import winsound
from PIL import Image
import telegram_send
import sys


cap = cv2.VideoCapture(0)

#hog = cv2.HOGDescriptor()
#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")
upper_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_upperbody.xml")    

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5
cont = 0
count = 0

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

while True:
    _, frame = cap.read()


    ret, frame = cap.read()
    ret, frame2 = cap.read()
    diff = cv2.absdiff(frame, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #print (type(diff))

    for c in contours:
        if cv2.contourArea(c) < 5000:
            cont = 0
        else:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)

            cont = 5




    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
    upper = upper_cascade.detectMultiScale(gray, 1.3, 5)

   

    #boxes,  weights =  hog.detectMultiScale(gray, winStride = (3, 3), padding = (8, 8), scale = 1.02)
    print("Size of Tuple1: " + str(sys.getsizeof(contours)) + "bytes")
    if  len(faces) +  len(bodies) + len(upper) > 0  or sys.getsizeof(contours) >240 :
        exact_time=datetime.now().strftime('%Y-%b-%d-%H-%S')
        cv2.imwrite('detected.jpg',frame)
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(
                f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording!")
            count=1

    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print('Stop Recording!')
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    if count == 1:
        current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        telegram_send.send(messages=["INTRUDER DETECTED AT: "+current_time])
        with open("detected.jpg", "rb") as f:
            telegram_send.send(images=[f],captions=[current_time])
        count = 0    

    for (x, y, width, height) in faces:
        cv2.rectangle(frame,(x, y), (x + width, y + height), (255, 0, 0), 3)
        img = cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
        exact_time=datetime.now().strftime('%Y-%m-%d----%H-%S')
        cv2.imwrite("face detected   "+str(exact_time)+".jpg",img)
    for (x, y, width, height) in bodies:
        cv2.rectangle(frame,(x, y), (x + width, y + height), (255, 0, 0), 3)
        cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2) 
    for (x, y, width, height) in upper:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)
        cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)    
    

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()