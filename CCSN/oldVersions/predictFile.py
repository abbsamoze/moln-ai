#import libraries 
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.layers import Input, Lambda, Dense, Flatten, Activation, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras import applications
from keras.models import load_model
import glob
import os.path
from pathlib import Path


def predictor(img):
    model = load_model('res.hdf5') #load .hdf5 file with all weights 
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #set picture to grayscale
    image = cv2.resize(image, (224, 224)) #resize to 244px X 244px
    image = np.array(image, dtype = 'float32')/255.0 # make it to precentage
    plt.imshow(image)
    image = image.reshape(1, 224,224,3)
    label_names = train_ds.class_indices #import labels on classes 
    dict_class = dict(zip(list(range(len(label_names))), label_names))
    clas = model.predict(image).argmax()
    name = dict_class[clas] # get clasname on predicted picture 
    altitude = DictForAltitude[clas] # get altitude on predicted picture
    estimate = DictForEstimate[clas] # get estimate on predicted picture
    print('The given image is of \nClass-number: {0} \nShape: {1}\nAltitude: {2}\nDescription: {3}'.format(clas, name, altitude, estimate)) #prints info of predicted image 
    
def getLastestPicture():
    folder_path = str(Path.home() / "Downloads") #path to local downloads 
    file_type = r'\*jpg' #search for jpg file 
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    return max_file #return latest filepath 

def predictOnLatest(): #function for predict lastest jpg img 
    latestPicture = getLastestPicture() 
    print(latestPicture)
    return predictor(f'{latestPicture}') #predict on latest picture 
    
    
    
def predictOnSelect(filename): #Predicts on selected filepath from website 
    return predictor(filename)

#Map clasnumber to altitude 
DictForAltitude = {
    4: 'High',
    2: 'High', 
    3: 'High', 
    0: 'Medium',
    1: 'Medium',
    7: 'Medium', 
    5: 'Low',
    6: 'Low',
    8: 'Low',
    9: 'Low'
    }

#Map clasnumber to weatherforcast prediction 
DictForEstimate = {
    4: 'The highest and least-substantial clouds. Composed of ice crystals, cirrus clouds lie at altitudes of about 45,000 feet. Wispy and lying at oblique angles, these clouds may herald the approach of a warm front.',
    2: 'Have barely-defined puffy balls and, like cirrostratus, lie at altitudes of 16,500 to 40,000 feet, usually in large clumps. From below, these clouds may look like fish scales. The saying "mackerel sky mackerel sky, not long wet, not long dry" describes them and the changeable weather that follows.', 
    3: 'Wispy clouds lying in sheets may form a ceiling slightly lower than cirrus clouds as a warm front nears and layers of cold air mix with upper warm air. May drape the entire sky in a gray haze and cause a halo around the sun or moon — an indication of a nearing storm.', 
    0: 'These have grayish-white rolls that look like cirrocumulus but are darker and sometimes appear in layers. If the wind is steady between northeast and south, these clouds promise rain soon.',
    1: 'Sheets of cloud between 6,000 and 23,000 feet. Thicker, darker and more claustrophobic than the higher cirrostratus clouds, they promise rain soon.',
    7: "Heavy, rain-laden, low-lying, dark gray blankets that come with warm fronts and wet nor'easters. Their soggy bases may be just above the earth's surface and be indistinguishable from heavy fog.", 
    5: "Dark, tightly-packed balls that may churn and tower as thunderheads at about 6,000 feet. If broader above than below, it's called an anvil head. This shape is due to violent updrafts through a wide range of temperatures. As the updraft hits, cold air is condensed as a cloud. Winds are strong around these threatening clouds.",
    6: 'Puffy white cotton balls at about 6,000 feet promise fair weather. They may, however, darken and be transformed into stratocumulus or cumulonimbus clouds, which can signal bad weather. Seen over land during the day indicates thermals and promises good sea breezes.',
    8: 'Large, dark, puffy balls occurring in compressed layers and foretell bad weather.',
    9: 'These clouds combine in a dense gray overcast that promises light to heavy rain.'
    }

image_size = (224, 224) 
batch_size = 16
train_datagen = ImageDataGenerator(rescale = 1./255,
    shear_range = 0.4,
    zoom_range = 0.4,
    horizontal_flip = True,
    vertical_flip = True,
    validation_split = 0.2)
train_ds = train_datagen.flow_from_directory('data/Train',
    target_size = image_size,
    batch_size = batch_size,
    class_mode = 'categorical',
    subset = 'training',
    color_mode="rgb",)

#predictOnLatest() <- returns prediction from latest download
#predictOnSelect("filepath") <- returns prediction on selcted file 