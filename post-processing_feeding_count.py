import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors
import time
import csv
import math

def incircle(x_test,y_test,x_circ,y_circ,rad_circ):
    if np.sqrt((x_test-x_circ)**2+(y_test-y_circ)**2) <= rad_circ:
        return 1
    else:
        return 0

def isactive(x_test):
    if math.isnan(x_test):
        return 0
    else:
        return 1

fps = 2 # FPS of the original video

path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"

os.chdir(path)
Dataframeorig = pd.read_hdf(os.path.join("data","20200712_paemula_cropDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5"))

Dataframe = Dataframeorig

file = path+"\\data\\img0259.pngfood.csv"
animalsfeeding = pd.DataFrame(index=Dataframe.index.values, columns=['time', 'sumfeeding', 'isactive'])
animalsfeeding['time'] = [x / (fps*60*60) for x in list(animalsfeeding.index)] # time in hours
animalsfeeding['sumfeeding'] = 0
animalsfeeding['isactive'] = 0

if os.path.isfile(file):
    with open(file, mode='r') as infile:
        file_reader = csv.reader(infile, delimiter=',', quotechar='"')
        # skip header
        next(file_reader)
        for line in file_reader:
            x_food,y_food,rad_food = [int(x) for x in line]
            # for animal in set(Dataframe.columns.get_level_values('individuals')):
            #     animalsfeeding['sumfeeding'] += Dataframe['DLC_resnet50_200714PaemulaJul14shuffle1_50000'][animal]['head'].apply(lambda row: incircle(row['x'], row['y'], x_food, y_food, rad_food), axis=1)
            print(line, " line")


            for animal in sorted(set(Dataframe.columns.get_level_values('individuals'))):
                print(animal)
                animalsfeeding['sumfeeding'] += Dataframe['DLC_resnet50_200714PaemulaJul14shuffle1_50000'][animal]['head'].apply(lambda row: incircle(row['x'], row['y'], x_food, y_food, rad_food), axis=1)

for animal in sorted(set(Dataframe.columns.get_level_values('individuals'))):
    animalsfeeding['isactive'] += Dataframe['DLC_resnet50_200714PaemulaJul14shuffle1_50000'][animal]['scutellum'].apply(lambda row: isactive(row['x']), axis=1)

animalsfeeding1 = animalsfeeding.copy()
animalsfeeding1['sumfeeding'] = animalsfeeding1['sumfeeding'].rolling(1200).mean()
animalsfeeding1['isactive'] = animalsfeeding1['isactive'].rolling(1200).mean()
animalsfeeding1.plot(x='time')
plt.show()
