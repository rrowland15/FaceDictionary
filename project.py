from PIL import Image
import pytesseract
import cv2 as cv
import matplotlib.pyplot as plt
import PIL

# load the face detection classifier
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# put together list of images
filenames = ["a-0.png", "a-1.png", "a-2.png", "a-9.png"]

glob_dict = {}

# iterate through the images in the file names list
for file in filenames:

    # convert the format and then enact the pytesseract method on each to recognize the text from the article.
    image = Image.open(file)
    image = image.convert('RGB')
    text = pytesseract.image_to_string(image.convert("L"))

    # convert the format and then enact the face_cascade method on each to recognize the faces from the article.
    img = cv.imread(file)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_boxes = face_cascade.detectMultiScale(gray, 1.31, minNeighbors=5)

    # put it all in a dictionary with the file being the key, DIDN'T NEED TO MAKE THESE LISTS.
    glob_dict[file] = ([image], [text], [face_boxes])
    
print(glob_dict.keys())
print(list(glob_dict.items())[0][0])

def wordsearch_and_buildsheet(word):
    """Param- takes a single word as an input"""
    """Returns- Face contact sheets for all of the newspaper images that contained the input word"""
    
    for key in range(len(glob_dict.keys())):

        if word in list(glob_dict.items())[key][1][1][0]:
            print("Results found in file {}".format(list(glob_dict.items())[key][0]))

            if len(list(glob_dict.items())[key][1][2][0]) == 0:
                print("But there were no faces in that file")

            else:
                
                crop_list = list(glob_dict.items())[key][1][2][0]
                l_crop_list = len(crop_list)
                
                x=0
                y=0

                start_w = list(glob_dict.items())[key][1][2][0][0][2]
                start_h = list(glob_dict.items())[key][1][2][0][0][3]
               
                contact_sheet = PIL.Image.new("RGB",(start_w*5,start_h*2),(0,0,0))
                
                for crops in range(l_crop_list):
                    
                    p1 = list(glob_dict.items())[key][1][2][0][crops][0]
                    p2 = list(glob_dict.items())[key][1][2][0][crops][1]
                    w = list(glob_dict.items())[key][1][2][0][crops][2]
                    h = list(glob_dict.items())[key][1][2][0][crops][3]
                  
                    face_img = Image.open(list(glob_dict.items())[key][0]).convert("RGB")
                    face_img = face_img.crop((p1,p2,p1+w,p2+h))
                    new_width = int((start_h/h)*w)
                    start_h = int(start_h)
                    
                    face_img = face_img.resize((new_width,start_h),Image.Resampling.LANCZOS)
                    contact_sheet.paste(face_img,(x,y))
                    
                    if x+new_width >= contact_sheet.width:
                        x = 0
                        y += start_h

                    else:
                        x += new_width

                contact_sheet = contact_sheet.save(str("people " + str(list(glob_dict.items())[key][0])))
                img = PIL.Image.open(str("people " + str(list(glob_dict.items())[key][0])))
                plt.imshow(img)
                plt.show()

    return None

#wordsearch_and_buildsheet("Christopher")
#wordsearch_and_buildsheet("fashion")
#wordsearch_and_buildsheet("water")
wordsearch_and_buildsheet("Detroit")





