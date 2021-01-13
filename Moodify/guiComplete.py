# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 19:26:14 2018

"""
import tkinter as tk
from tkinter import *
import cv2
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense,MaxPooling2D,Flatten,Dropout,Conv2D

model = keras.models.load_model("Final_Model_categories_3.model")

choice=1

import time
from PIL import ImageTk, Image
def callfunc(list1):
    def makeWindow () :
        
        win = Tk()
    
        frame1 = Frame(win)
        frame1.pack()
    
        win.title('song')
        Label(frame1, text='Enter song number', width = 30, height = 10).grid(row=0)
        e1 = Entry(frame1)
        e1.grid(row=0, column=1)
        
        frame2 = Frame(win)       # Row of buttons
        frame2.pack()
        b1 = Button(frame2,text=" Click  ",bg = 'yellow',foreground = 'green',command = lambda : func(int(e1.get())))
        b1.pack(side = LEFT)
    
        frame3 = Frame(win)       # select of names
        frame3.pack()
        scroll = Scrollbar(frame3, orient=VERTICAL)
        mylist = Listbox(frame3, yscrollcommand = scroll.set )
        for i in range(0,len(list1)):
           mylist.insert(END,str(i) +". "+ list1[i])
        
        scroll.config (command=mylist.yview)
        scroll.pack(side=RIGHT, fill=Y)
        mylist.pack(side=LEFT,  fill=BOTH, expand=1)
        return win
    def func(ch):
        global choice
        wind.destroy()
        choice=ch
    
    global choice
    wind = makeWindow()
    
    wind.mainloop()
    return choice
    
    

def splashscreen () :
    
    window = Tk()
    window.title('MOODIFY')

    F1 = Frame(window)
    F1.pack()
    l1 = Label(F1, text='" MOODIFY "',height = 2, width = 37, font = 'coopergothicbold', bg = 'black', foreground ='orange')
    l1.pack()
        
    l2 = Label(F1, text = 'YOUR MOOD , YOUR MUSIC',height = 2, width = 37,font = 'cooperblack', bg = 'black', foreground = 'white')
    l2.pack()
    
    img = ImageTk.PhotoImage(Image.open("mood.png"))
    l3 = Label(F1, image = img, bg ='black')
    l3.img=img
    l3.pack()
    #l3.pack(side = 'bottom', fill= 'both', expand = 'yes')
    
    return window

def CaptureImage():
        
    print("Take an image : \n")
    cap=cv2.VideoCapture(0)


    while(1):
    

        _,frame2=cap.read()
        frame2 = cv2.flip(frame2,1)
        cv2.imshow("frame",frame2)
    
        x=cv2.waitKey(5)
        if x==ord('c'):
    
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            frame2=cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(frame2, 1.3, 5)
            for (x,y,w,h) in faces:
                 frame2 = frame2[y:y+h, x:x+w]
            
            cv2.imwrite("img.jpeg",frame2)
            cv2.waitKey(5)
            break
        
    cv2.destroyAllWindows()
    cap.release()
    wind.destroy()


def startWindow() :
    
    window = splashscreen()
    window.update()
    time.sleep(2)
    window.destroy()
    time.sleep(0.5)
    
    
    wind = Tk()
    wind.title('capture image')

    f1 = Frame(wind)
    f1.pack()
    label1 = Label(f1, text='PRESS OKAY TO\n CAPTURE IMAGE\n ', width = 29, height = 3, font = 'algerian', bg = 'gold')
    label1.pack()
    
    f2 = Frame(wind)
    f2.pack()
    button = Button(f2, text='Okay', bg ='forest green',foreground = 'gold', font = 'algerian',command = CaptureImage)
    #button = Button(command = f2.destroy)
    #button.grid(row = 1, rowspan = 2, sticky = 'E')
    button.pack()
    
    f1 = Frame(wind)
    f1.pack()
    label2 = Label(f1, text='After that press "c" to capture \n\t\t\t\t\t\t', bg = 'gold')
    label2.pack()
    
    return wind

wind = startWindow()

wind.mainloop()


#for offline mode
def offline():
    wind.destroy()
    import numpy as np
    from keras.preprocessing import image
    test_image = image.load_img('img.jpeg', target_size = (64, 64),grayscale=1)
    
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)
    itunes=os.listdir("SONGS")
    if result[0][0] == 1:
        y=3
        
        print("\nYou seem Excited :(\n ")
        prediction="Excited"
        songs=os.listdir("SONGS/"+itunes[y])
        x=callfunc(songs)
        subprocess.run(["open","-a","/Applications/itunes.app","SONGS/"+itunes[y]+"/"+songs[x]])
        print("Playing song " + songs[x])
        
        
         
        
    
    if result[0][1]==1:
        
        
        prediction="Happy"
        print("You seem Happy :) \n ")
        y=1
        songs=os.listdir("SONGS/"+itunes[y])
        x=callfunc(songs)
        subprocess.run(["open","-a","/Applications/itunes.app","SONGS/"+itunes[y]+"/"+songs[x]])
        print("Playing song "  + songs[x])
        
        
    if result[0][2]==1:
        
        print("\nYou seem Sad :( \n ")
        prediction="Sad"
        y=2
        songs1=os.listdir("SONGS/"+itunes[y])
        x=callfunc(songs1)
        subprocess.run(["open","-a","/Applications/itunes.app","SONGS/"+itunes[y]+"/"+songs1[x]])
        print("Playing song " + songs1[x])
       

#for online mode
def online():
   
    wind.destroy()
    import numpy as np
    from keras.preprocessing import image
    try:
        test_image = image.load_img('img.jpeg', target_size = (64, 64),grayscale=1)
        
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = model.predict(test_image)
    except OSError:
        print("Failed! Try Again")
    
    import webbrowser
     
    happy = ['POP','EDM','Jazz','IndieRock']
    sad = ['Instrumental','POP','Rock','Deep','classic']
    Excited = ['EDM','House','HIP-HOP','Disco']
    
    if result[0][1] ==1 :
        print('!!--You seem Happy please select your favourite genre--!!')
        prediction="Happy"
        x=callfunc(happy)
        if x == 0:
            webbrowser.open('https://www.youtube.com/watch?v=pgN-vvVVxMA&list=PLDcnymzs18LU4Kexrs91TVdfnplU3I5zs&start_radio=1')
        elif x== 1:
            webbrowser.open('https://www.youtube.com/watch?v=lTx3G6h2xyA&list=PLUg_BxrbJNY5gHrKsCsyon6vgJhxs72AH&start_radio=1')
        elif x==2:
            webbrowser.open('https://www.youtube.com/watch?v=21LGv8Cf0us&list=PLMcThd22goGYit-NKu2O8b4YMtwSTK9b9&start_radio=1')
        elif x==3:
            webbrowser.open('https://www.youtube.com/watch?v=VQH8ZTgna3Q&list=PLVAJ90ZhCcL896CZDbuIz2HGKeVekfEee&start_radio=1')
        else:
            webbrowser.open('https://www.youtube.com')
            
        print("Playing " + happy[x])
            
    elif result[0][2] == 1:
        x=callfunc(sad)
        print('!!--You Seem Sad please select your favourite genre--!!')
        prediction="Sad"
        if x == 0:
            webbrowser.open('https://www.youtube.com/watch?v=Pa__NZaRXxs&list=PLIWSikhI2_z2lNqsfjF4ahut28056cJtz')
        elif x== 1:
            webbrowser.open('https://www.youtube.com/watch?v=pgN-vvVVxMA&list=PLDcnymzs18LU4Kexrs91TVdfnplU3I5zs&start_radio=1')
        elif x==2:
            webbrowser.open('https://www.youtube.com/watch?v=6Ejga4kJUts&list=PLhd1HyMTk3f5PzRjJzmzH7kkxjfdVoPPj&start_radio=12')
        elif x==3:
            webbrowser.open('https://www.youtube.com/watch?v=UAWcs5H-qgQ&list=PLzzwfO_D01M4nNqJKR828zz6r2wGikC5a')
        elif x==4:
            webbrowser.open('https://www.youtube.com/watch?v=4Tr0otuiQuU&list=RDQMqk8OvYGJVWM&start_radio=1')
        else:
            webbrowser.open('https://www.youtube.com')
        print("Playing " + sad[x])
            
        
    elif result[0][0] == 1:
        x=callfunc(Excited)
        print('!!--You seem Excited please select your favourite genre--!!')
        prediction="Exciting"
        if x == 0:
            webbrowser.open('https://www.youtube.com/watch?v=lTx3G6h2xyA&list=PLUg_BxrbJNY5gHrKsCsyon6vgJhxs72AH&start_radio=1')
        elif x== 1:
            webbrowser.open('https://www.youtube.com/watch?v=BDocp-VpCwY&list=PLhInz4M-OzRUsuBj8wF6383E7zm2dJfqZ&start_radio=1')
        elif x==2:
            webbrowser.open('https://www.youtube.com/watch?v=xTlNMmZKwpA&start_radio=1&list=PLH6pfBXQXHEC2uDmDy5oi3tHW6X8kZ2Jo')
        elif x==3:
            webbrowser.open('https://www.youtube.com/watch?v=kJQP7kiw5Fk&list=PL64E6BD94546734D8')
        else:
            webbrowser.open('https://www.youtube.com')
        print("Playing " + Excited[x])
    else:
        webbrowser.open('https://www.youtube.com/watch?v=aJOTlE1K90k&list=PLw-VjHDlEOgvtnnnqWlTqByAtC7tXBg6D')
    
pred=" "
def quits():
    wind.destroy()


def SecondWindow () :
    import numpy as np
    from keras.preprocessing import image


    test_image = image.load_img('img.jpeg', target_size = (64, 64),grayscale=1)
        
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)
    if result[0][0]==1:
        pred="Excited"
    elif result[0][1]==1:
        pred="Happy"
    elif result[0][2]==1:
        pred="Sad"
   
    
    
    
    
    
    wind = Tk()
    wind.title('MOODIFY')
    Frame(bg = 'tan1',height = 15)

    f1 = Frame(wind)
    f1.grid()
    Label(f1, text='CHOOSE THE MODE IN WHICH\n YOU WANT TO LISTEN THE SONG ', width = 29, height = 3, font = 'algerian', bg = 'tan1').grid(row=0, rowspan = 1)
    
    f2 = Frame(wind)
    f2.grid(row = 1, column = 0, columnspan = 2)
    button1 = Button(f2, text='Offline', bg = 'White',foreground = 'Gold', relief = 'sunken', command = offline).grid(row = 1,column = 0,columnspan = 2 )
    button2 = Button(f2, text='Online', bg = 'White',foreground = 'Gold',  relief = 'sunken', command =online).grid(row = 1,column = 2,columnspan = 2)
    button2 = Button(f2, text='quit', bg = 'White',foreground = 'Gold',  relief = 'sunken', command =quits).grid(row = 1,column = 4,columnspan = 2)
        
    f4 = Frame(wind)
    f4.grid()
    Label(f4, text="You seem " + pred, bg = 'tan1', height =3).grid(row = 2)
    
    return wind

wind = SecondWindow()

wind.mainloop()



    


