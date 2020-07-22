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

def analysis(h5file, foodcsv, fps, rollingwindow):
    # the DLC h5 output is a multiindex pandas dataframe
    input_df = pd.read_hdf(h5file)

    input_df[input_df.columns[0][0],'all','analysis','time'] = [x / (fps*60*60) for x in list(input_df.index)] # time in hours
    input_df[input_df.columns[0][0],'all','analysis','isactive'] = 0

# count 'head' occurences in feeding spots individually
    if os.path.isfile(foodcsv):
        with open(foodcsv, mode='r') as infile:
            file_reader = csv.reader(infile, delimiter=',', quotechar='"')
            # skip header
            next(file_reader)
            # get food locations
            for i, line in enumerate(file_reader):
                x_food,y_food,rad_food = [int(x) for x in line]
                print("calculating presence in spot: ", line)
                # make separate column for each food spot
                input_df[input_df.columns[0][0],'all','analysis','sumfeeding_'+str(i)] = 0
                for animal in sorted(set(input_df.columns.get_level_values('individuals')[input_df.columns.get_level_values('individuals') != 'all'])):
                    print(animal)
                    input_df[input_df.columns[0][0],'all','analysis','sumfeeding_'+str(i)] += input_df[input_df.columns[0][0]][animal]['head'].apply(lambda row: incircle(row['x'], row['y'], x_food, y_food, rad_food), axis=1)
                # make rollig mean to smooth dataframe
                input_df[input_df.columns[0][0],'all','analysis','sumfeeding_'+str(i)] = input_df[input_df.columns[0][0],'all','analysis','sumfeeding_'+str(i)].rolling(rollingwindow).mean()

    # 'scutellum' is the most robust for beetles as it is in the middel --> use this for general activity
    print("calculating sum of general activity... ")
    for animal in sorted(set(input_df.columns.get_level_values('individuals')[input_df.columns.get_level_values('individuals') != 'all'])):
        input_df[input_df.columns[0][0],'all','analysis','isactive'] += input_df[input_df.columns[0][0]][animal]['scutellum'].apply(lambda row: isactive(row['x']), axis=1)
        print(animal)
    input_df[input_df.columns[0][0],'all','analysis','isactive'] = input_df[input_df.columns[0][0],'all','analysis','isactive'].rolling(rollingwindow).mean()
    return input_df

if __name__ == '__main__':
    # do something
    path="D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"
    os.chdir(path)
    file = os.path.join(path,"data","200710_paemula_crop_sampleDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5")
    foodcsv = os.path.join(path,"data","200710_paemula_crop_sample_stillframe.pngfood.csv")
    animalsfeeding = analysis(file, foodcsv, 2, 1200)
    animalsfeeding[animalsfeeding.columns[0][0],'all','analysis'].plot(x='time')
    plt.show()
