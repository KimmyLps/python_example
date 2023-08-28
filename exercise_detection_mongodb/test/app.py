
#!/usr/bin/env python
# -- coding: utf-8 --
import tkinter as tk
from tkinter import messagebox
# from PIL import Image, ImageTk  # install pillow with pip: pip install pillow
import datetime
import time
import csv, os
# import pandas as pd

credential_file = "credential.csv"

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
 
        #load = Image.open("img1.jpg")
        #photo = ImageTk.PhotoImage(load)
        #label = tk.Label(self, image=photo)
        #label.image = photo
        #label.place(x=0, y=0)
 
        border = tk.LabelFrame(
            self, text='Login', bg='ivory', bd=10, font=("Arial", 20))
        border.pack(fill="both", expand="yes", padx=150, pady=150)
 
        username_lb = tk.Label(border, text="Username",
                          font=("Arial Bold", 15), bg='ivory')
        username_lb.place(x=50, y=20)
        Txt1 = tk.Entry(border, width=30, bd=5)
        Txt1.place(x=180, y=20)
 
        Label2 = tk.Label(border, text="Password",
                          font=("Arial Bold", 15), bg='ivory')
        Label2.place(x=50, y=80)
        TXT2 = tk.Entry(border, width=30, show='*', bd=5)
        TXT2.place(x=180, y=80)
 
        def verify():
            try:
                with open(credential_file, "r") as f:
                    info = f.readlines()
                    i = 0
                    for e in info:
                        u, p, cd, md = e.split(",")
                        if u.strip() == Txt1.get() and p.strip() == TXT2.get():
                            controller.show_frame(SecondPage)
                            i = 1
                            break
                    if i == 0:
                        messagebox.showinfo(
                            "Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo(
                    "Error", "Please provide correct username and password!!")
 
        BTN1 = tk.Button(border, text="Submit",
                         font=("Arial", 15), command=verify)
        BTN1.place(x=250, y=130)
 
        def register():
            window = tk.Tk()
            window.resizable(0, 0)
            window.configure(bg="deep sky blue")
            window.title("Register")
            username_lb = tk.Label(window, text="Username:", font=(
                "Arial", 15), bg="deep sky blue")
            username_lb.place(x=10, y=10)
            username = tk.Entry(window, width=30, bd=5)
            username.place(x=200, y=10)
 
            pass_lb = tk.Label(window, text="Password:", font=(
                "Arial", 15), bg="deep sky blue")
            pass_lb.place(x=10, y=60)
            password = tk.Entry(window, width=30, show="*", bd=5)
            password.place(x=200, y=60)
 
            confirm_pass_lb = tk.Label(window, text="Confirm Password:",
                            font=("Arial", 15), bg="deep sky blue")
            confirm_pass_lb.place(x=10, y=110)
            confirm_pass = tk.Entry(window, width=30, show="*", bd=5)
            confirm_pass.place(x=200, y=110)

            def check():
                # Set values to variable
                Username = (username.get())
                Password = (password.get())
                ConfirmPass = (confirm_pass.get())

                ts = time.time()
                created_date = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                if (Username.strip() and Password.strip() and ConfirmPass.strip()):
                    if (Password == ConfirmPass):

                        headerList = ['Username', 'Password', 'Created Date', 'Modified Date']

                        with open(credential_file, "a", encoding='UTF8', newline='') as csvFile:

                            # If first create file or file is empty add header to file
                            if os.path.isfile(credential_file):
                                if os.stat(credential_file).st_size==0:
                                    dw = csv.DictWriter(csvFile, delimiter=',', fieldnames=headerList)
                                    dw.writeheader()
                            
                            # Write data to file
                            rows = [Username, Password, created_date, created_date]
                            writer = csv.writer(csvFile)
                            writer.writerow(rows)

                             # Show message success
                            messagebox.showinfo(
                                "Welcome", "You are registered successfully!!")
                    else:
                        messagebox.showinfo(
                            "Error", "Your password didn't get match!!")
                else:
                    if Username.strip()==False:
                        messagebox.showinfo(
                        "Error", "Please Enter the Username!!")
                    elif (Password.strip()==False or ConfirmPass.strip()==False):
                        messagebox.showinfo(
                        "Error", "Please enter the password or confirm password!!")

                    messagebox.showinfo(
                        "Error", "Please enter your username and password!!")
 
            btn1 = tk.Button(window, text="Sign up", font=(
                "Arial", 15), bg="#ffc22a", command=check)
            btn1.place(x=170, y=150)
 
            window.geometry("470x220")
            window.mainloop()
 
        BTN2 = tk.Button(self, text="Register", bg="dark orange",
                         font=("Arial", 15), command=register)
        BTN2.place(x=690, y=200)
 
 
class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
 
        #load = Image.open("img2.jpg")
        #photo = ImageTk.PhotoImage(load)
        #label = tk.Label(self, image=photo)
        #label.image = photo
        #label.place(x=0, y=0)
        
        #self.configure(bg='Tomato')
        
        Label = tk.Label(self, text="ยินดีต้อนรับ! \n\n โปรแกรมกายภาพบำบัดโรคหลอดเลือดสมอง \n\n คณะวิศวกรรมศาสตร์ มหาวิทยาลัยนราธิวาสราชนครินทร์", 
                         bg="orange", font=("TH Sarabun New", 25, 'bold'))
        Label.place(relx=.5, rely=.5,anchor= 'center')

        Button = tk.Button(self, text="Next", font=(
            "Arial", 15), command=lambda: controller.show_frame(ThirdPage))
        Button.place(x=870, y=540)
 
        Button = tk.Button(self, text="Back", font=(
            "Arial", 15), command=lambda: controller.show_frame(FirstPage))
        Button.place(x=70, y=540)

def openWindow():
    #หน้าจอ2
    #myWindow = Tk()
    #myWindow.title("การฝึกกายภาพ")
    #myWindow.geometry("500x500")
    import cv2               #pip install cv2 
    import mediapipe as mp   #pip install mediapipe
    import numpy as np       #pip install numpy

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # 3. calculate angle
    def calculate_angle(a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    # 4.
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)

                # Visualize angle
                cv2.putText(image, str(angle),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # Curl counter logic
                if angle > 160:
                    stage = "down"
                if angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1
                    print("counter is: ", counter)
                    now = datetime.today()
                    f1= open("result.txt","a")
                    f1.write(now.ctime()+", Counter is: %d\r\n" % counter +"\n")
                    #f1.close()
                    #with open("result.txt","w+") as f1:
                    #    f1.write(now.ctime(), "Counter is: %d\r\n" % counter)

            except:
                pass

            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

            # Rep data
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (65, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, stage,
                        (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                    )
            
            cv2.imshow('Mediapipe Feed', image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
 
        Label = tk.Label(self, text="ผลการฝึกกายภาพบำบัด", bg="orange", font=("JasmineUPC Bold", 20))
        Label.place(x=40, y=30)

        Button = tk.Button(self, text="Home", font=(
            "Arial", 15), command=lambda: controller.show_frame(FirstPage))
        Button.place(x=870, y=540)
 
        Button = tk.Button(self, text="Back", font=(
            "Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=70, y=540)

        Button = tk.Button(self, text="เริ่มกายภาพ",bg="green", font=(
            "JasmineUPC Bold", 25), command=openWindow)
        Button.place(x=800, y=30)

        Label = tk.Label(self, text="ชื่อ-สกุล: ",  font=("JasmineUPC Bold", 18))
        Label.place(x=40, y=80)
        f = open("credential.txt", "r")
        Label = tk.Label(self, text=f.read(),  font=("JasmineUPC Bold", 18))
        Label.place(x=130, y=80)
        f2 = open("result.txt", "r")
        Label = tk.Label(self, text=f2.read(),  font=("Arial", 12))
        Label.place(x=40, y=120)

 
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
 
        # creating a window
        window = tk.Frame(self)
        window.pack()
 
        window.grid_rowconfigure(0, minsize=600)
        window.grid_columnconfigure(0, minsize=1000)
 
        self.frames = {}
        for F in (FirstPage, SecondPage, ThirdPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
 
        self.show_frame(FirstPage)
 
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")

app = Application()
app.maxsize(1440, 940)
app.mainloop()