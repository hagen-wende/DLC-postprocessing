import analysis
import getfoodlocation
import helperfunctions

import glob
import os.path
import pandas as pd
import matplotlib.pyplot as plt
import datetime

####################################################
#### collect and prepare data ######################
#### mark foodlocation for all videos if not present

# collect all project file names in a Dataframe
df_project = helperfunctions.getprojectfiles()

if df_project is None:
    print("#########################################################")
    print("Video or h5 files are missing, please make sure that both")
    print("a video file and the corresponding h5 file are present.")
    print("#########################################################")
else:
    # extract still frame from each video
    df_project['stillframes'] = helperfunctions.extractframes(df_project)

    # check whether there is a food file if not label food sources
    df_project['foodcsvs'] = getfoodlocation.markfood(df_project)

    ###################
    #### Analysis #####
    # general activity
    #   number of animals active
    # presence at food pots
    #   total
    #   comparison between different food sources


    # for short videos rollingwindow must be reduced!!!
    rollingwindow = 600 #  2 = 1 second @fps=2; 120 = 1 min
    starttime = 8 # starttime of video in hours
    fps = 2
    bodyparts = ['head', 'scutellum'] # for which bodyparts feeding should be calculated
    bodypartforactivity = 'scutellum'
    df_alldata = pd.DataFrame()

    # go over all h5 files and analyse them
    for h5file in df_project['h5files']:
        if h5file:

            animalsfeeding = analysis.feeding(h5file, df_project, fps, bodyparts)
            animalsactive = analysis.activity(h5file, fps, bodypartforactivity)

            combined_df = pd.concat([animalsfeeding, animalsactive])
            # plotactivity graph
            analysis.plotactivity(h5file, combined_df, rollingwindow, starttime)

            df_alldata = pd.concat([df_alldata, combined_df])
        else:
            print("no data to analyse for ", df_project['videos'][df_project.index[df_project['h5files'] == h5_file]][0])


    # save analysed dataset and project to csv
    outfilepath = df_project['h5files'][0].rsplit('\\',1)[0]

    df_alldata.to_csv(outfilepath+"/output_df.csv")
    df_project.to_csv(outfilepath+"/project_df.csv")


##############
# TODO List ##
##############
# general
# smoothing trajectories
# interpolating missing values
# presence at feed pots
#   duration of visit
#   summation and statistics of results
# activity
#   resting vs moving
