import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from PIL import ImageTk, Image 
#from tkinter.filedialog import asksaveasfile 
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import messagebox


import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import shutil
from PIL import ImageGrab
#this is for dividing the process
from subprocess import *
import subprocess
import time



#window design and geometry---------------------------------------------------------------------
root = Tk()
root.title('FACE RECOGNITION')
root.geometry('800x450')



frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )
#-----------------------------------------------------------------------------------------------



#dummy fuction-----------------------------------------------------------
def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()
#------------------------------------------------------------------------

#functions to save a file-------------------------------------------------
def open_img(): 
    x = openfilename() 
    img = Image.open(x)
    img = img.resize((250, 250), Image.ANTIALIAS) 
    img = ImageTk.PhotoImage(img) 
    panel = Label(root, image = img) 
    panel.place(x=390, y=90)   
    panel.image = img 

def openfilename(): 
   
    root.filename = filedialog.askopenfilename(title ='open file')
    global y
    y=root.filename
     
    return root.filename
    


def displaypicmsg():
    shutil.copy(y,'faceimages')
    messagebox.showinfo("Sucess","Picture Uploaded Successfully!!!")     
       
#------------------------------------------------------------------------    

#function to find encodings----------------------------------------------
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
#--------------------------------------------------------------------------


#gace recognition function-------------------------------------------------
def facereg():


    import time
    progress['value']=20
    root.update_idletasks()
    time.sleep(7)
    progress['value']=50
    root.update_idletasks()
    time.sleep(1)


    video_capture = cv2.VideoCapture(0)
 
    path = 'faceimages'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    

#just to make sure encodings are done-----------------------------
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')  
#-------------------------------------------------------------------


    progress['value']=80
    root.update_idletasks()

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    time.sleep(1)
    progress['value']=100
    messagebox.showinfo("IMPORTANT","PRESS 'Q' TO CLOSE FACIAL RECOGNITION")
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(encodeListKnown, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = classNames[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

#-----------------------------------------------------------------------------------------------


#following is the function to run onscreen face detection(ayush along with shambus)
#=================================================-------=======================================

def facescriptreg():


    import time
      
    progress['value']=20
    root.update_idletasks()
    time.sleep(7)
    progress['value']=50
    root.update_idletasks()
    time.sleep(1)
  

    video_capture = cv2.VideoCapture(0)
 
    path = 'faceimages'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    


    encodeListKnown = findEncodings(images)
    print('Encoding Complete')  


    progress['value']=80
    root.update_idletasks()

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    time.sleep(1)
    progress['value']=100
    
    messagebox.showinfo("IMPORTANT","PRESS 'Q' TO CLOSE FACIAL RECOGNITION")
   # here the a new process is started
    

    
    pname=ename.get()
    plocation=eloc.get()

    nquery='python auto_script.py'+' '+pname+' '+plocation 
    Popen(nquery)
    time.sleep(3)

    
    while True:

      
        img = ImageGrab.grab()
        img_np = np.array(img)

        frame = cv2.cvtColor(img_np,cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        if process_this_frame:
            
            face_locations = face_recognition.face_locations(rgb_small_frame,number_of_times_to_upsample=2)
            # model='cnn'
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
               
                matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
                name = "Unknown"

               
                face_distances = face_recognition.face_distance(encodeListKnown, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = classNames[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame
        
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
           

            face_scrape = []

            for pers in face_names:
                if not pers=="Unknown":
                    face_scrape.append(pers)



            for person_name in face_scrape:
                     
                try:
                     roi_color = frame[top:bottom, left:right] 
                     print("[INFO] Object found. Saving locally.") 
                     cv2.imwrite('scrapped_img/'+person_name+str(right) + str(bottom) + '_faces.jpg', roi_color)
                except Exception:
                     print("No face in this image")

           
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
       
        cv2.imshow('Video', frame)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    
    video_capture.release()
    cv2.destroyAllWindows()

#================================================--------========================================






#progressbar elements--------------------------------------------------------------------------

s=Style()
s.configure("TProgressbar",foreground="red",background="red",thickness=40)


label1=Label(bottomframe,font="arial 15 bold")
label1.pack(side = BOTTOM)

progress=Progressbar(bottomframe,orient = HORIZONTAL,length=400,mode='determinate')
progress.pack(side = BOTTOM)

#----------------------------------------------------------------------------------------------







#background------------------------------------------
canvas = Canvas(width=350, height=200, bg='blue')
canvas.pack(expand=YES, fill=BOTH)
image = ImageTk.PhotoImage(file="faceback1.jpg")
canvas.create_image(0, 0, image=image, anchor=NW)
#----------------------------------------------------





#menubar------------------------------------------------------------------------
menubar = Menu(root)
#filemenu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


#edit menu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)


#help menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)


root.config(menu=menubar)

#---------------------------------------------------------------------------------------


#/////////////////////////////////////////////////////////////////////////////////////


#buttons-----------------------------------------------------------------------------------


hel = tkFont.Font(family='CORNERSTONE', size=10, weight=tkFont.BOLD)
comi= tkFont.Font(family='Comic Sans MS', size=10, weight=tkFont.BOLD)


""" 
b=Button(root)
photo=PhotoImage(file="red11.png")
b.config(image=photo,text="enter",width="100",height="40")
b.place(relx = 0.1, rely = 0.5)
b.pack()
"""


#select picture button
x1=Button(root,text="Select an image",command = lambda : open_img(),font=hel)
x1.config(width="27",height="2",bg="#E74C3C ",activebackground="#EC7063")
x1.place(x = 40,y = 60)


""" 
#shambus script button
scr=Button(root,text="Find on Social Media",font=hel)
scr.config(width="27",height="2",bg="#E74C3C ",activebackground="#EC7063")
scr.place(x = 40,y = 140)

 """

#real time face recog
x2=Button(root,text="Real time Face Recognition",font=hel,command=facereg)
x2.config(width="27",height="2",bg="#2ECC71",activebackground="#1D8348")
x2.place(x = 40,y = 130)


#onscreen face recog(ayush+shambu)
x3=Button(root,text="On Screen Face Recognition",font=hel,command=facescriptreg)
x3.config(width="27",height="2",bg="#2ECC71",activebackground="#1D8348")
x3.place(x = 40, y = 320)


#display message button and save image
b1=Button(root,font=hel,text="CONFIRM",width="10",height="1",bg="#2980B9",activebackground="#F9E79F",command=displaypicmsg)
b1.place(x=460,y=350)


#exit button
btn1=Button(root,font=hel,text="EXIT",width="13",height="2",bg="#F4D03F",activebackground="#F9E79F",command=root.quit)
btn1.place(x = 680, y = 320) 


#------------------------------------------------------------------------------------------------------------------------------------




#textbox--------------------------------------------------------------------



ename=Entry(root,width=30)
ename.place(x = 40, y = 220)
ename.insert(0,"Enter the name")


eloc=Entry(root,width=30)
eloc.place(x = 40, y = 280)
eloc.insert(0,"Enter the location")




#-----------------------------------------------------------------------------




#////////////////////////////////////////////////////////////////////////////////////
root.mainloop()