from gtts import gTTS
import os

# for windows only
from playsound import playsound

import speech_recognition as sr
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300

import cv2 as cv
import numpy as np
import face_recognition 
import os
from datetime import datetime
import time


threshold = 0.58  # Experiment with this value
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    if cl == '.DS_Store':
        continue
    curImg = cv.imread(f'{path}/{cl}')
    if curImg is None:
        print(f'Image not loaded correctly: {path}/{cl}')
        continue
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0]) # getting Iris Wang instead of Iris Wang.jpg

print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        print(myDataList)
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

encodeListKnown = findEncodings(images)
print('the encodings are completed, number of encodings are:')
print(len(encodeListKnown))

def removeFalseAttendance(name):
    with open('Attendance.csv', 'r') as f:
        lines = f.readlines()
    
    with open('Attendance.csv', 'w') as f:
        for line in lines:
            if line.strip("\n").split(",")[0] != name:
                f.write(line)

def newFace(): 
    global encodeListKnown
    newfacegreet()
    print('Hello student! This is Professor Hamid!')
    print('I have never seen you before.')

    with sr.Microphone() as source:
        print("what is your name:")
        audio_data = recognizer.listen(source,timeout=10)
        try:
            print("You said: " + recognizer.recognize_google(audio_data))
            correct = input("Is that correct? \nType 'Y' / 'N' to confirm: ").upper()
            if(correct == 'Y'):
                name = recognizer.recognize_google(audio_data)
                newfacegreet2(name)
                time.sleep(2)
                valid_name = name.replace(" ", "_")
                new_image_path = f"{path}/{valid_name}.jpg"
                cv.imwrite(new_image_path, img)
                # Add the new image and name to the existing lists
                images.append(cv.imread(new_image_path))
                classNames.append(valid_name)
                # Update the known encodings
                encodeListKnown = findEncodings(images)
                print('Encodings updated!')
                markAttendance(name)
            else:
                print('Failed to get the name.')
                name = input('Please type your name to register: ').upper()
                newfacegreet2(name)
                time.sleep(2)
                valid_name = name.replace(" ", "_")
                new_image_path = f"{path}/{valid_name}.jpg"
                cv.imwrite(new_image_path, img)
                # Add the new image and name to the existing lists
                images.append(cv.imread(new_image_path))
                classNames.append(valid_name)
                # Update the known encodings
                encodeListKnown = findEncodings(images)
                print('Encodings updated!')
                markAttendance(name)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
        except sr.RequestError:
            print("Speech Recognition service request failed")
    return encodeListKnown 

cap = cv.VideoCapture(0)
#if not cap.isOpened():
#    print("Could not open webcam")
#    exit()

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio_data = recognizer.listen(source, timeout=10)
        try:
            text = recognizer.recognize_google(audio_data)  # Using Google's speech recognition
            return text
        except:
            print("Sorry, I could not understand the audio")
            return None

def text_to_speech(text):
    try:
        # Convert text to speech
        tts = gTTS(text=text, lang='en')
        audio_path = "temp_audio.mp3"
        tts.save(audio_path)
        
        # Play the generated audio
        playsound(audio_path)
        
        # Optionally, remove the generated audio file after playing
        os.remove(audio_path)
        
    except Exception as e:
        print(f"An error occurred: {e}")

count = 0

def newfacegreet():
    text = f'Hello student! This is Professor Hamid! I have never seen you before. What is your name?'
    text_to_speech(text)

def newfacegreet2(name):
    text = f'Hi {name}, nice to meet you! I will remember you from now'
    text_to_speech(text)


def greet(name):
    text = f'Good Morning {name}, Very good to see you!'
    text_to_speech(text)

name_counts = {}
greeted_names = set()


while True:
    success, img = cap.read()
    imgS = cv.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame): # grab encode and face location from
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] < threshold:
            count = 0
            name = classNames[matchIndex].upper()

            if name in name_counts:
                name_counts[name] += 1
            else:
                name_counts[name] = 1

            print(f"{name}: {name_counts[name]}")  # Add this print statement

            # If the count reaches the threshold, greet the person and reset the count
            if name_counts[name] == 5 and name not in greeted_names: 
                greeted_names.add(name)
                name_counts[name] = 0  # Reset the count
                greet(name)
    
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv.rectangle(img,(x1,y1),(x2,y2),(150, 65, 233),2)
            cv.rectangle(img,(x1,y2-35),(x2,y2),(150, 65, 233), cv.FILLED)
            cv.putText(img,name,(x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1,(255,255,255),2)
            markAttendance(name)
            
        elif count == 5:
            name2 = '?'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv.rectangle(img, (x1, y1), (x2, y2), (105, 190, 22), 2)
            cv.rectangle(img, (x1, y2-35), (x2, y2), (105, 190, 22), cv.FILLED)
            encodeListKnown = newFace()
            count = 0
        else:
            count = count+1
            name2 = '?'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv.rectangle(img, (x1, y1), (x2, y2), (105, 190, 22), 2)
            cv.rectangle(img, (x1, y2-35), (x2, y2), (105, 190, 22), cv.FILLED)
            cv.putText(img, name2, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            

    cv.imshow('Webcam', img)
    key = cv.waitKey(1)
    if key == 27: # Press ESC key to exit
        break

cap.release()
cv.destroyAllWindows()
