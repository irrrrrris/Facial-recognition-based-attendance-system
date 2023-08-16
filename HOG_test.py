import cv2 as cv
import numpy as np
import face_recognition 

imgIris1 = face_recognition.load_image_file('/Users/irisjiayiwang/Desktop/OPENCV/Faces/train/Iris Wang/17.jpg')
imgIris1 = cv.cvtColor(imgIris1, cv.COLOR_BGR2RGB)

imgIris2 = face_recognition.load_image_file('/Users/irisjiayiwang/Desktop/OPENCV/Faces/train/Justin Cui/11.jpg')
imgIris2 = cv.cvtColor(imgIris2, cv.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imgIris1)[0]
encodeIris = face_recognition.face_encodings(imgIris1)[0]
cv.rectangle(imgIris1,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]), (255, 0, 255),2) 
# faceLoc gives the 4 corner points of the face detected

faceLoc = face_recognition.face_locations(imgIris2)[0]
encodeTest = face_recognition.face_encodings(imgIris2)[0]
cv.rectangle(imgIris2,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]), (255, 0, 255),2) 

results = face_recognition.compare_faces([encodeIris], encodeTest)
faceDis = face_recognition.face_distance([encodeIris], encodeTest)
print(results, faceDis)
cv.putText(imgIris2, f'{results} {round(faceDis[0],2)}', (50,50), cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

cv.imshow('Iris1',imgIris1)
cv.imshow('Iris2',imgIris2)
cv.waitKey(0)