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

def feeding(h5file, df_project, fps, bodyparts):
    # the DLC h5 output is a multiindex pandas dataframe
    input_df = pd.read_hdf(h5file)
    # get foodsource(s)
    foodcsv = df_project.at[df_project.index[df_project['h5files'] == h5file][0],'foodcsvs']

    # we could also drop this level, since we are not using it
    scorer = input_df.columns[0][0]

    # convert frames to time in hours from index
    input_df[scorer,'all','analysis','time'] = [x / (fps*60*60) for x in list(input_df.index)]

    # count 'head' and 'scutellum occurences in feeding spots individually
    if os.path.isfile(foodcsv):
        with open(foodcsv, mode='r') as infile:
            file_reader = csv.reader(infile, delimiter=',', quotechar='"')
            # skip header
            next(file_reader)
            # loop over food locations
            for i, line in enumerate(file_reader):
                x_food, y_food, rad_food = [int(x) for x in line[:3]]
                foodtype = line[3]
                print("calculating presence in spot: ", line)
                input_df[scorer,'all','analysis','sumfeeding_'+foodtype] = 0 #create new column for feeding sum over all animals
                for animal in sorted(set(input_df.columns.get_level_values('individuals')[input_df.columns.get_level_values('individuals') != 'all'])):
                    print("for ",animal)
                    # check whether the bodyparts are within the food circle and add 0/1 for each animal
                    for bodypart in bodyparts:
                        input_df[scorer,animal,bodypart,'sumfeeding_'+foodtype] = input_df[scorer][animal][bodypart].apply(lambda row: incircle(row['x'], row['y'], x_food, y_food, rad_food), axis=1)

                    # feeding sum for all animals
                    input_df = input_df.sort_index(axis=1) # otherwise raises performance issue
                    input_df[scorer,'all','analysis','sumfeeding_'+foodtype] += input_df.xs('sumfeeding_'+foodtype, axis=1, level=3, drop_level=False)[scorer,animal][bodyparts].max(axis=1)
    else:
        print("No food file for ", h5file, " found.")
    return input_df

if __name__ == '__main__':
    # dataset for testing module
    path="D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"
    os.chdir(path)
    file = os.path.join(path,"data","200710_paemula_crop_sampleDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5")
    foodcsv = os.path.join(path,"data","200710_paemula_crop_sample_stillframe.pngfood.csv")
    animalsfeeding = feeding(file, foodcsv, 2)

    animalsfeeding[animalsfeeding.columns[0][0],'all','analysis'].plot(x='time')
    plt.show()
