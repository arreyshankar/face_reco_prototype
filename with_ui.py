import tkinter as tk
import tkinter.messagebox
import cv2

path = "C:/Users/sarvesh/Desktop/face_reco_prototype/Training_images"
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
    window.mainloop()


def imageCapture():
    cam = cv2.VideoCapture(0)
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
            cv2.imwrite("./Training_images/"+img_name, frame)
            print("{} saved ".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()