import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors
import time
import cv2

### GUI to select food source
path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing\\video"

os.chdir(path)
image = plt.imread('img0259.png')
implot = plt.imshow(image)

# show image
fig, ax=plt.subplots()
ax.imshow(image)

# select point
yroi = plt.ginput(0,0)

#print(yroi)
time.sleep(5)
