import tkinter as tk
import pandas as pd
import numpy as np
import re
import pymongo
import tkinter.messagebox
import face_recognition
from PIL import Image
from PIL import ImageTk
import csv
import threading
import datetime
import imutils
import cv2
import os


client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client['mevo']
collection = database['records']
cam = cv2.VideoCapture(0)
path = "C:/Users/sarvesh/Desktop/face_reco_prototype/Images"
records_path = "C:/Users/sarvesh/Desktop/face_reco_prototype/Records.csv"
window = tk.Tk()
Name = tk.StringVar()
Age = tk.StringVar()
Gender = tk.StringVar()

images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    
def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

def readRecord(name):
    id = re.findall(r'\d+',name)
    id = int(id[0])
    
    result = collection.find_one({'id':int(id)})
    
    #df = pd.read_csv(records_path)
    #result = df[df["id"] == id]
    
    Pid = result['id']
    PName = result['Name']
    PAge = result['Age']
    pGender = result['Gender']
    tkinter.messagebox.showinfo("Details",""+str(Pid)+"\t"+PName+"\t"+str(PAge)+"\t"+pGender)
    
def getDetails():
    cam = cv2.VideoCapture(0)
    imgname = ''
    while True:
        success, img = cam.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                imgname = classNames[matchIndex]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, imgname, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)        
    
        cv2.imshow('Webcam', img)
        k = cv2.waitKey(3000) & 0xff 
        if k == 27:
            break
    cam.release()
    readRecord(imgname)
    

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

def writeRecord(id,name,age,gender):
    
    record = {'id':id , 'Name':name , 'Age':int(age) , 'Gender':gender}
    collection.insert_one(record)
    
    #with open(records_path, mode='a', newline='') as records:
    #    records.write('\n')
    #    writer = csv.writer(records, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #    writer.writerow([id, name, age, gender])

def registeration():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Press Space to Capture and ESC to quit")
    img_counter = 0
    id = collection.count_documents({})+1
    name = Name.get()
    age = Age.get()
    gender = Gender.get()
    
    writeRecord(id,name,age,gender)
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            img_name = str(id)+"_"+str(Name.get())+"_{}.png".format(img_counter)
            cv2.imwrite("./Images/"+img_name, frame)
            print("{} saved ".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

    
if __name__ == "__main__":
    GUI_init()