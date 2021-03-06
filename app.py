import cv2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from PIL import Image
import PIL.ImageOps
import os, ssl, time
x = np.load('image.npz')['arr_0']
y = pd.read_csv('labels.csv')['labels']
xtrain,xtest,ytrain,ytest = train_test_split(x,y,random_state = 9,train_size = 7500,test_size = 2500)
xtrainScaled = xtrain/255
xtestScaled = xtest/255
clf = LogisticRegression(solver = 'saga',multi_class='multinomial').fit(xtrainScaled,ytrain)
def getPrediction(image):
    im_pil = Image.open(image)
    # convert to grayscale image - 'L' format means each pixel is 
    # represented by a single value from 0 to 255
    image_bw = im_pil.convert('L')
    image_bw_resized = image_bw.resize((22,30), Image.ANTIALIAS)
    image_bw_resized_inverted = PIL.ImageOps.invert(image_bw_resized)
    pixel_filter = 20
    min_pixel = np.percentile(image_bw_resized_inverted, pixel_filter)
    image_bw_resized_inverted_scaled = np.clip(image_bw_resized_inverted-min_pixel, 0, 255)
    max_pixel = np.max(image_bw_resized_inverted)
    image_bw_resized_inverted_scaled = np.asarray(image_bw_resized_inverted_scaled)/max_pixel
    test_sample = np.array(image_bw_resized_inverted_scaled).reshape(1,660)
    test_pred = clf.predict(test_sample)
    return test_pred[0]