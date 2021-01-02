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

def activity(h5file, fps, bodypart):
    # the DLC h5 output is a multiindex pandas dataframe
    input_df = pd.read_hdf(h5file)
    # we could also drop this level, since we are not using it
    scorer = input_df.columns[0][0]

    # calculate time from index if not already there
    input_df[scorer,'all','analysis','time'] = [x / (fps*60*60) for x in list(input_df.index)] # time in hours

    # new column for activity/presence
    input_df[scorer,'all','analysis','isactive'] = 0

    print("calculating sum of general activity... ")
    for animal in sorted(set([level for level in input_df.columns.get_level_values('individuals') if level != 'all'])):
        print(animal)
        input_df[scorer,animal,bodypart,'isactive'] = input_df[scorer][animal][bodypart].apply(lambda row: isactive(row['x']), axis=1)
        input_df[scorer,'all','analysis','isactive'] += input_df[scorer][animal][bodypart].apply(lambda row: isactive(row['x']), axis=1)
    return input_df.sort_index(axis=1)

## todo: generalize output for different scenarios and put into a module
def plotactivity(h5file, input_df, rollingwindow, starttime):
    print("making activity plot ... ")
    # we could also drop this level, since we are not using it
    scorer = input_df.columns[0][0]

    for condition in sorted(set([level for level in input_df.columns.get_level_values('coords') if level not in ['time', 'x', 'y', 'likelihood']])):
        # make rollig mean to smooth data
        input_df[scorer,'all','rollingmean',condition] = input_df[scorer,'all','analysis',condition].rolling(rollingwindow).mean()

    # convert time to time of day starting from start of video (8 am)
    input_df[scorer,'all','analysis','daytime'] = input_df[scorer,'all','analysis','time'] + starttime

    fig = plt.figure()
    fig.suptitle('Animal activity', fontsize=30)
    fig.set_size_inches(5*2.54, 2.5*2.54)
    ax1 = fig.add_subplot()
    fig.patch.set_facecolor('#e2e2e2')
    ax1.set_facecolor('#bebebe')

    input_df = input_df.sort_index(axis=1)
    colors = ['#08ae27', '#000076', '#f70606']

    # plot one line for each condition
    for i, condition in enumerate(sorted(set([level for level in input_df.columns.get_level_values('coords') if level not in ['time','daytime', 'x', 'y', 'likelihood']]))):

        ax1.plot(input_df[scorer,'all','analysis']['daytime'], input_df[scorer,'all','rollingmean'][condition], colors[i], zorder = i, label=condition)

    ax1.set_xlabel("time (hours)", fontsize=17)
    ax1.set_ylabel("# of animals", rotation=90, fontsize=17)
    ax1.tick_params(axis='both', which='major', labelsize=15)
    leg = ax1.legend(loc='upper right', shadow=True)

    fig.savefig(h5file+'_activity.png', facecolor=fig.get_facecolor())

if __name__ == '__main__':
    # test data
    path="D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"
    os.chdir(path)
    file = os.path.join(path,"data","200710_paemula_crop_sampleDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5")
    animalsfeeding = activity(file, 2)

    animalsfeeding[animalsfeeding.columns[0][0],'all','analysis'].plot(x='time')
    plt.show()
