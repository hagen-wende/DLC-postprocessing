import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors
import time
import csv
import math

def isactive(x_test):
    if math.isnan(x_test):
        return 0
    else:
        return 1

def activity(h5file, fps):
    # the DLC h5 output is a multiindex pandas dataframe
    input_df = pd.read_hdf(h5file)

    input_df[input_df.columns[0][0],'all','analysis','time'] = [x / (fps*60*60) for x in list(input_df.index)] # time in hours
    input_df[input_df.columns[0][0],'all','analysis','isactive'] = 0

    # 'scutellum' is the most robust for beetles as it is in the middel --> use this for general activity
    print("calculating sum of general activity... ")
    for animal in sorted(set(input_df.columns.get_level_values('individuals')[input_df.columns.get_level_values('individuals') != 'all'])):
        input_df[input_df.columns[0][0],animal,'scutellum','isactive'] = input_df[input_df.columns[0][0]][animal]['scutellum'].apply(lambda row: isactive(row['x']), axis=1)
        input_df[input_df.columns[0][0],'all','analysis','isactive'] += input_df[input_df.columns[0][0]][animal]['scutellum'].apply(lambda row: isactive(row['x']), axis=1)
        print(animal)
    return input_df.sort_index(axis=1)

if __name__ == '__main__':
    # do something
    path="D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"
    os.chdir(path)
    file = os.path.join(path,"data","200710_paemula_crop_sampleDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5")
    animalsfeeding = activity(file, 2)

    animalsfeeding[animalsfeeding.columns[0][0],'all','analysis'].plot(x='time')
    plt.show()
