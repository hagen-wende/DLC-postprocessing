import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors
import time
import csv

def incircle(x_test,y_test,x_circ,y_circ, rad_circ):
    if np.sqrt((x_test-x_circ)**2+(y_test-y_circ)**2) <= rad_circ:
        return 1
    else:
        return 0

path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"

os.chdir(path)
Dataframeorig = pd.read_hdf(os.path.join("data","20200711_paemula_cropDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5"))

Dataframe = Dataframeorig

x_food=558
y_food=387
rad_food=68

animalsfeeding = pd.DataFrame(index=Dataframe.index.values, columns=['time', 'sumfeeding'])
animalsfeeding['time'] = [x / (180*60) for x in list(animalsfeeding.index)]
animalsfeeding['sumfeeding'] = 0
for animal in sorted(set(Dataframe.columns.get_level_values('individuals'))):
    print(animal)
    animalsfeeding['sumfeeding'] += Dataframe['DLC_resnet50_200714PaemulaJul14shuffle1_50000'][animal]['head'].apply(lambda row: incircle(row['x'], row['y'], x_food, y_food, rad_food), axis=1)


animalsfeeding.plot(x='time')
plt.show()
