#!/usr/bin/env python
# coding: utf-8

# # The Project #
# 1. This is a project with minimal scaffolding. Expect to use the the discussion forums to gain insights! It’s not cheating to ask others for opinions or perspectives!
# 2. Be inquisitive, try out new things.
# 3. Use the previous modules for insights into how to complete the functions! You'll have to combine Pillow, OpenCV, and Pytesseract
# 4. There are hints provided in Coursera, feel free to explore the hints if needed. Each hint provide progressively more details on how to solve the issue. This project is intended to be comprehensive and difficult if you do it without the hints.
# 
# ### The Assignment ###
# Take a [ZIP file](https://en.wikipedia.org/wiki/Zip_(file_format)) of images and process them, using a [library built into python](https://docs.python.org/3/library/zipfile.html) that you need to learn how to use. A ZIP file takes several different files and compresses them, thus saving space, into one single file. The files in the ZIP file we provide are newspaper images (like you saw in week 3). Your task is to write python code which allows one to search through the images looking for the occurrences of keywords and faces. E.g. if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions "pizza". This will test your ability to learn a new ([library](https://docs.python.org/3/library/zipfile.html)), your ability to use OpenCV to detect faces, your ability to use tesseract to do optical character recognition, and your ability to use PIL to composite images together into contact sheets.
# 
# Each page of the newspapers is saved as a single PNG image in a file called [images.zip](./readonly/images.zip). These newspapers are in english, and contain a variety of stories, advertisements and images. Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use [small_img.zip](./readonly/small_img.zip) for testing.
# 
# Here's an example of the output expected. Using the [small_img.zip](./readonly/small_img.zip) file, if I search for the string "Christopher" I should see the following image:
# ![Christopher Search](./readonly/small_project.png)
# If I were to use the [images.zip](./readonly/images.zip) file and search for "Mark" I should see the following image (note that there are times when there are no faces on a page, but a word is found!):
# ![Mark Search](./readonly/large_project.png)
# 
# Note: That big file can take some time to process - for me it took nearly ten minutes! Use the small one for testing.

# In[1]:


import zipfile
import PIL
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!


# In[2]:


from zipfile import ZipFile
files='readonly/small_img.zip'
filenames=[]

with ZipFile(files,'r') as zip:
    #display the files in the zip
    zip.printdir()
    #extract files from the zip
    zip.extractall()
    for info in zip.infolist():
        filenames.append(info.filename)
print(filenames)


# In[ ]:


glob_dict={}

for file in filenames:
    image=Image.open(file)
    image=image.convert('RGB')
    print(file)
    text=pytesseract.image_to_string(image.convert("L"))
    #print(text)
    img=cv.imread(file)
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    face_boxes = face_cascade.detectMultiScale(gray,1.31,minNeighbors=5)
    #face_boxes = face_cascade.detectMultiScale(img,1.35)
    #print(face_boxes)
    
    glob_dict[file]=([image],[text],[face_boxes])
    
print(glob_dict.keys())


# In[5]:


#keys=glob_dict.keys()
#print(list(glob_dict.items())[0][1][2][0][0])
#print(list(glob_dict.items())[0][1][1][0])
print(list(glob_dict.items())[0][0])

def wordsearch_and_buildsheet(word): 
    
    for key in range(len(glob_dict.keys())):
        
        if word in list(glob_dict.items())[key][1][1][0]:
            print("Results found in file {}".format(list(glob_dict.items())[key][0]))
            if len(list(glob_dict.items())[key][1][2][0])==0:
                print("But there were no faces in that file")
            else:
                
                crop_list=list(glob_dict.items())[key][1][2][0]
                l_crop_list=len(crop_list)
                
                x=0
                y=0
                start_w=list(glob_dict.items())[key][1][2][0][0][2]
                start_h=list(glob_dict.items())[key][1][2][0][0][3]
               
                contact_sheet=PIL.Image.new("RGB",(start_w*5,start_h*2),(0,0,0))
                
                for crops in range(l_crop_list):
                    
                    p1=list(glob_dict.items())[key][1][2][0][crops][0]
                    p2=list(glob_dict.items())[key][1][2][0][crops][1]
                    w=list(glob_dict.items())[key][1][2][0][crops][2]
                    h=list(glob_dict.items())[key][1][2][0][crops][3]
                  
                    face_img=Image.open(list(glob_dict.items())[key][0]).convert("RGB")
                    face_img=face_img.crop((p1,p2,p1+w,p2+h))
                    new_width=int((start_h/h)*w)
                    start_h=int(start_h)
                    
                    face_img=face_img.resize((new_width,start_h),Image.ANTIALIAS)
                    contact_sheet.paste(face_img,(x,y))
                    
                    if x+new_width >= contact_sheet.width:
                        x=0
                        y=y+start_h
                    else:
                        x=x+new_width
                display(contact_sheet)
    
                
    return None

wordsearch_and_buildsheet("Christopher")


# In[6]:


from zipfile import ZipFile
files='readonly/images.zip'
filenames=[]

with ZipFile(files,'r') as zip:
    #display the files in the zip
    zip.printdir()
    #extract files from the zip
    zip.extractall()
    for info in zip.infolist():
        filenames.append(info.filename)
print(filenames)


# In[ ]:


glob_dict={}

for file in filenames:
    image=Image.open(file)
    image=image.convert('RGB')
    print(file)
    text=pytesseract.image_to_string(image.convert("L"))
    #print(text)
    img=cv.imread(file)
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    face_boxes = face_cascade.detectMultiScale(gray,1.31,minNeighbors=5)
    #face_boxes = face_cascade.detectMultiScale(img,1.35)
    #print(face_boxes)
    
    glob_dict[file]=([image],[text],[face_boxes])
    
print(glob_dict.keys())


# In[8]:


#keys=glob_dict.keys()
#print(list(glob_dict.items())[0][1][2][0][0])
#print(list(glob_dict.items())[0][1][1][0])
print(list(glob_dict.items())[0][0])

def wordsearch_and_buildsheet(word): 
    
    for key in range(len(glob_dict.keys())):
        
        if word in list(glob_dict.items())[key][1][1][0]:
            print("Results found in file {}".format(list(glob_dict.items())[key][0]))
            if len(list(glob_dict.items())[key][1][2][0])==0:
                print("But there were no faces in that file")
            else:
                
                crop_list=list(glob_dict.items())[key][1][2][0]
                l_crop_list=len(crop_list)
                
                x=0
                y=0
                start_w=list(glob_dict.items())[key][1][2][0][0][2]
                start_h=list(glob_dict.items())[key][1][2][0][0][3]
               
                contact_sheet=PIL.Image.new("RGB",(start_w*5,start_h*2),(0,0,0))
                
                for crops in range(l_crop_list):
                    
                    p1=list(glob_dict.items())[key][1][2][0][crops][0]
                    p2=list(glob_dict.items())[key][1][2][0][crops][1]
                    w=list(glob_dict.items())[key][1][2][0][crops][2]
                    h=list(glob_dict.items())[key][1][2][0][crops][3]
                  
                    face_img=Image.open(list(glob_dict.items())[key][0]).convert("RGB")
                    face_img=face_img.crop((p1,p2,p1+w,p2+h))
                    new_width=int((start_h/h)*w)
                    start_h=int(start_h)
                    
                    face_img=face_img.resize((new_width,start_h),Image.ANTIALIAS)
                    contact_sheet.paste(face_img,(x,y))
                    
                    if x+new_width >= contact_sheet.width:
                        x=0
                        y=y+start_h
                    else:
                        x=x+new_width
                display(contact_sheet)
    
                
    return None

wordsearch_and_buildsheet("Mark")


# In[1]:





# In[ ]:




