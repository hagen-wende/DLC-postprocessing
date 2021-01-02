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
    bodypartforheatmap = 'head'

    df_alldata = pd.DataFrame()

    # go over all h5 files and analyse them
    for h5file in df_project['h5files']:
        if h5file:
            print("Analysing ", h5file.rsplit('\\',1)[1])
            # analyse feeding and activity
            feedingoutput_df = analysis.feeding(h5file, df_project, fps, bodyparts)
            activityoutput_df = analysis.activity(h5file, fps, bodypartforactivity)
            combined_df = feedingoutput_df.merge(activityoutput_df, how='left')

            # plotactivity graph
            analysis.plotactivity(h5file, combined_df, rollingwindow, starttime)

            # generate heatmaps
            heatmap = analysis.createheatmap(h5file, df_project, bodypartforheatmap, gausssize=51)
            analysis.saveheatmapwithfood(heatmap, h5file, df_project, bodypartforheatmap)

            videofilename = df_project['videos'][df_project.index[df_project['h5files'] == h5file]].values[0].rsplit('\\',1)[1]

            # combines results from the different experiments using the videofilename as an additional multiindex level
            try: # if df_alldata contains data
                df_alldata = pd.merge([df_alldata, pd.concat({videofilename: combined_df}, names=['videofilename'], axis=1)], how='left')
            except TypeError: # if df_alldata is still empty
                df_alldata = pd.concat([df_alldata, pd.concat({videofilename: combined_df}, names=['videofilename'], axis=1)], axis=1)
        else:
            print("no data to analyse for ", df_project['videos'][df_project.index[df_project['h5files'] == h5_file]][0])

            pd.concat({combined_df.columns[0][0]: combined_df}, names=[h5file], axis=1)

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
