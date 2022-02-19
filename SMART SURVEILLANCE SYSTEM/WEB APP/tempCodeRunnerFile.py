import numpy as np
import telegram_send
import cv2,time
from datetime  import datetime
import winsound
from PIL import Image
import telegram_send
import os,sys
from flask import Flask, render_template, Response, request
from threading import Thread

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")
upper_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_upperbody.xml")    


global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0



count = 0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass



app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)

frame_size = (int(camera.get(3)), int(camera.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")



def detect_face(frame,frame2):
    detection = False
    detection_stopped_time = None
    timer_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 5

    

    
    diff = cv2.absdiff(frame, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #print (type(diff))

    for c in contours:
        if cv2.contourArea(c) < 5000:
            pass
            
        else:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)

     




    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
    upper = upper_cascade.detectMultiScale(gray, 1.3, 5)

   

    #boxes,  weights =  hog.detectMultiScale(gray, winStride = (3, 3), padding = (8, 8), scale = 1.02)
    #print("Size of Tuple1: " + str(sys.getsizeof(contours)) + "bytes")
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
    frame = cv2.flip(frame, 1)
    try:
        #frame=frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = ( int(w * r), 480)
        frame=cv2.resize(frame,dim)
    except Exception as e:
        pass
    
    return frame
 

def gen_frames():  # generate frame by frame from camera
    
    global out, capture,rec_frame
    while True:
        success, frame = camera.read()
        success, frame2 = camera.read()  
        if success:
            if(face):                
                frame= detect_face(frame,frame2)
            if(grey):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if(neg):
                frame=cv2.bitwise_not(frame)    
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
        elif  request.form.get('grey') == 'Grey':
            global grey
            grey=not grey
        elif  request.form.get('neg') == 'Negative':
            global neg
            neg=not neg
        elif  request.form.get('face') == 'Face Only':
            global face
            face=not face 
            if(face):
                time.sleep(4)   
        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1
        elif  request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                #Start new thread for recording the video
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()
                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
    
camera.release()
out.release()
cv2.destroyAllWindows()     

