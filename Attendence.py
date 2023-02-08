import os
import cv2
import csv
import numpy as np
import face_recognition
from datetime import datetime
from twilio.rest import Client
import keys

path=r'C:\Users\HP\COMPUTER VISION\Face Recognition\images'


images=[]
classNames=[]

mylist=os.listdir(path)



for cl in mylist:
    currentimage=cv2.imread(f'{path}/{cl}')
    images.append(currentimage)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findencoding(images):
    encodelist=[]
    for img in images:
        image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(image)[0]
        encodelist.append(encode)
    return encodelist    
encodelistknownfaces=findencoding(images)

f=open('Attendence.csv','r+',newline='')


present_lst=[]
cap=cv2.VideoCapture(0)
while True:
    sucess,img=cap.read()
    imagesmall=cv2.resize(img,(0,0),None,0.25,0.25)
    faceinframe=face_recognition.face_locations(imagesmall)
    faceencode=face_recognition.face_encodings(imagesmall,faceinframe)
    

    for faceEncode,faceLoc in zip(faceencode,faceinframe):
        matches=face_recognition.compare_faces(encodelistknownfaces,faceEncode)
        facedistance=face_recognition.face_distance(encodelistknownfaces,faceEncode)
      
        matchindex=np.argmin(facedistance)

        if matches[matchindex]:
            name=classNames[matchindex]
           

            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4  

            cv2.rectangle(img,(x1,y1),(x2,y2),color=(0,255,0),thickness=3)
            cv2.rectangle(img,(x1,y1-30),(x2,y1),(0,0,0),thickness=-1)
            cv2.putText(img,name,(x1,y1),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0),3)
            cv2.putText(img,'Attendence marked',(x1,y1+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            if name not in present_lst:
                present_lst.append(name)
                print('match :',matches)
                print('face distance :',facedistance)
                print(name)
                
                now= datetime.now()
                current_date=now.strftime('%Y-%m-%d')
                
                current_time=now.strftime('%H:%M:%S')
                time=('14:57:00')
                if current_time<time:
                    status='ontime'
                else:
                    status='latecome'
    
                f.writelines(f'{name},{current_date},{current_time},{status}\n')
                


       
    cv2.imshow('face',img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

print('today presents is:',present_lst) 
k=open('Absent.csv','w+',newline='') 
absent_lst=[] 
for cn in classNames:
          if cn not in present_lst:
              status='absent'
              k.writelines(f'{cn},{status}\n')
              absent_lst.append(cn)
          else:
              pass
print('today absents is:',absent_lst)


client=Client(keys.account_sid,keys.auto_token)
for i in absent_lst:
    if i=='jeff bezos':
        message=client.messages.create(
            body='your son/daughter '+i+' is absent today.why?',
            from_=keys.twilio_number,
            to=keys.my_number)
       
        
       
