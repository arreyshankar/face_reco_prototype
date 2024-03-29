import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from pymongo.server_api import ServerApi
import re
from bson.binary import Binary
import pymongo
import tkinter.messagebox
import face_recognition
import cv2
import os

uri = "mongodb+srv://sarvesh:mevo123@testingcluster.tg9uqrx.mongodb.net/?retryWrites=true&w=majority&appName=TestingCluster"
client = pymongo.MongoClient(uri,server_api=ServerApi('1'))
database = client['mevo']
record_collection = database['records']
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS,60)
cam.set(cv2.CAP_PROP_BUFFERSIZE,30)
window = tk.Tk()
Name = tk.StringVar()
Age = tk.StringVar()
Gender = tk.StringVar()

encodeList = []
Images = []
pIds = []
pNames = []
pAges =[]
pGenders = []
pImages = []


def init_encoding():
    for document in record_collection.find():
        pIds.append(document['_id'])
        pNames.append(document['Name'])
        pAges.append(document['Age'])
        pGenders.append(document['Gender'])
        pImages.append(document['Image'])

    for image in pImages:
        nparr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        Images.append(img)

    for img in Images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

def readRecord(id):
    result = record_collection.find_one({'_id':int(id)})
    
    Pid = result['_id']
    PName = result['Name']
    PAge = result['Age']
    pGender = result['Gender']
    pImage = result['Image']
    nparr = np.frombuffer(pImage, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    imgS = cv2.resize(image, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    tkinter.messagebox.showinfo("Details","\nID: "+str(Pid)+"\nName: "+PName+"\nAge: "+str(PAge)+"\nGender: "+pGender)
    
def getDetails():
    init_encoding()
    cam = cv2.VideoCapture(0)
    imgname = ''
    while True:
        success, img = cam.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeList, encodeFace)
            faceDis = face_recognition.face_distance(encodeList, encodeFace)
            matchIndex = np.argmin(faceDis)
            print(matchIndex)
            if matches[matchIndex]:
                id = pIds[matchIndex]
                Name = pNames[matchIndex]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
                cv2.putText(img, Name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)        
                print("ID :: ",id)
        cv2.imshow('Webcam', img)
        k = cv2.waitKey(3000) & 0xff 
        if k == 27:
            break
    cam.release()
    readRecord(id)

def GUI_init():
    window.minsize(800,600)

    frame1 = tk.Frame(master=window, width=250, bg="#178E92")
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    textView1 = tk.Label(master=frame1,text="Name: ")
    textView1.pack(side=tk.TOP,padx=10,pady=10)
    name = tk.Entry(master=frame1,textvariable=Name, width=50)
    name.pack(side=tk.TOP,padx=10,pady=10)
    textView2 = tk.Label(master=frame1,text="Age: ")
    textView2.pack(side=tk.TOP,padx=10,pady=10)
    age = tk.Entry(master=frame1,textvariable=Age, width=50)
    age.pack(side=tk.TOP,padx=10,pady=10)
    textView3 = tk.Label(master=frame1,text="Gender: ")
    textView3.pack(side=tk.TOP,padx=10,pady=10)
    gender = tk.Entry(master=frame1,textvariable=Gender, width=50)
    gender.pack(side=tk.TOP,padx=10,pady=10)
    register = tk.Button(master=frame1,text="Register",command = registeration)
    register.pack(side=tk.TOP)

    frame2 = tk.Frame(master=window, width=250, bg="#5CAD4B")
    frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    textView5 = tk.Label(master=frame2,text="Get Patient Details")
    textView5.pack(side=tk.LEFT,padx=10)
    getDetailsButton = tk.Button(master=frame2,text="Get Details",command=getDetails)
    getDetailsButton.pack(side=tk.LEFT,padx=10) 
    window.mainloop()

def writeRecord(id,name,age,gender,image_data):
    
    record = {'_id':id , 'Name':name , 'Age':int(age) , 'Gender':gender , 'Image':image_data}
    record_collection.insert_one(record)

def registeration():
    cam = cv2.VideoCapture(0)
    id = record_collection.count_documents({})+1
    name = Name.get()
    age = Age.get()
    gender = Gender.get()
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Press Space to Capture and ESC to quit", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            _, image_data = cv2.imencode('.jpg', frame)
            image_binary = Binary(image_data.tobytes())
            writeRecord(id,name,age,gender,image_binary)
            tkinter.messagebox.showinfo("Alert","Registration Successfull")
    
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    init_encoding()
    GUI_init()