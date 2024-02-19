import tkinter as tk
import tkinter.messagebox
#from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import csv
import threading
import datetime
import imutils
import cv2
import os

cam = cv2.VideoCapture(0)
path = "C:/Users/sarvesh/Desktop/face_reco_prototype/Images"
records_path = "C:/Users/sarvesh/Desktop/face_reco_prototype/Records.csv"
window = tk.Tk()
imageTitle = tk.StringVar()

def main():
    window.minsize(800,600)

    frame1 = tk.Frame(master=window, width=250, bg="#178E92")
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    textView = tk.Label(master=frame1,text="Name: ")
    textView.pack(side=tk.LEFT,padx=10)
    name = tk.Entry(master=frame1,textvariable=imageTitle, width=50)
    
    name.pack(side=tk.LEFT,padx=10)
    register = tk.Button(master=frame1,text="Register",command = imageCapture)
    register.pack(side=tk.LEFT)

    frame2 = tk.Frame(master=window, width=250, bg="#5CAD4B")
    frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    textView2 = tk.Label(master=frame2,text="Get Patient Details")
    textView2.pack(side=tk.LEFT,padx=10)
    getDetailsButton = tk.Button(master=frame2,text="Get Details",command=getDetails)
    getDetailsButton.pack(side=tk.LEFT,padx=10) 
    window.mainloop()


def imageCapture():
   
    cv2.namedWindow("Press Space to Capture and ESC to quit")
    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = str(imageTitle.get())+"_{}.png".format(img_counter)
            cv2.imwrite("./Images/"+img_name, frame)
            print("{} saved ".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()


def getDetails():
    image1 = Image.open("./Images/sarvesh_0.png")   
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(image=test,master=window)
    label1.image = test
    label1.pack(side=tk.TOP)
    
    with open(records_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            #if 
            print([col + '=' + row[col] for col in reader.fieldnames])

if __name__ == "__main__":
    main()