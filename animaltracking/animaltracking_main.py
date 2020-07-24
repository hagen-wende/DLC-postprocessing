import analysis
import getfoodlocation
# import analysis.feedingcount as feedingcount
# import analysis.activity as activity
from tkinter import Tk
from tkinter.filedialog import askdirectory
import glob
import os.path
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def getvideos():
    root = Tk()
    root.wm_attributes('-topmost', 1) # opens windows in front
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    foldername = askdirectory() # show an "Open" dialog box and return the path to the selected file
    videos = glob.glob(os.path.join(foldername, '*.mp4'))
    root.destroy()
    return videos

def extractframe(video_name):

    vidObj = cv2.VideoCapture(video_name)

    if not vidObj.isOpened():
        print("could not open: ",video_name)
        return

    # get number of frames of the video
    length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))

    # get frame in the middle of the vid
    vidObj.set(cv2.CAP_PROP_POS_FRAMES,round(length/2));
    ret, frame = vidObj.read()

    # Cut the video extension to have the name of the video
    my_video_name = video.split(".")[0]

    # save frame
    cv2.imwrite(my_video_name+'_stillframe.png', frame)

def plotactivity(h5file, animalsdf, rollingwindow, starttime):
    # make rollig mean to smooth data
    animalsdf[animalsdf.columns[0][0],'all','analysis','sumfeeding_0'] = animalsdf[animalsdf.columns[0][0],'all','analysis','sumfeeding_0'].rolling(rollingwindow).mean()
    animalsdf[animalsdf.columns[0][0],'all','analysis','sumfeeding_1'] = animalsdf[animalsdf.columns[0][0],'all','analysis','sumfeeding_1'].rolling(rollingwindow).mean()
    animalsdf[animalsdf.columns[0][0],'all','analysis','isactive'] = animalsdf[animalsdf.columns[0][0],'all','analysis','isactive'].rolling(rollingwindow).mean()

    # convert time to time of day starting from start of video (8 am)
    animalsdf[animalsdf.columns[0][0],'all','analysis','time'] = animalsdf[animalsdf.columns[0][0],'all','analysis', 'time']+8

    fig = plt.figure()
    fig.suptitle('Pachnoda aemula activity', fontsize=20)
    fig.set_size_inches(5*2.54, 2.5*2.54)
    ax1 = fig.add_subplot()
    fig.patch.set_facecolor('#e2e2e2')
    ax1.set_facecolor('#bebebe')
    #ax1.set_ylim(min(y_values)-1,max(y_values)+1)
    #ax1.set_xlim(0,7)

    # plot regress line
    l1, = ax1.plot(animalsdf[animalsdf.columns[0][0],'all','analysis']['time'], animalsdf[animalsdf.columns[0][0],'all','analysis']['sumfeeding_0'], '#08ae27', zorder = 1)
    l2, = ax1.plot(animalsdf[animalsdf.columns[0][0],'all','analysis']['time'], animalsdf[animalsdf.columns[0][0],'all','analysis']['sumfeeding_1'], '#000076', zorder = 2)
    l3, = ax1.plot(animalsdf[animalsdf.columns[0][0],'all','analysis']['time'], animalsdf[animalsdf.columns[0][0],'all','analysis']['isactive'], '#f70606', zorder = 3)

    ax1.set_xlabel("time (hours)", fontsize=17)
    ax1.set_ylabel("# of beetles", rotation=90, fontsize=17)
    ax1.legend((l1, l2, l3), ('beetles feeding on artificial diet', 'beetles feeding on banana', 'active beetles'), loc='upper right', shadow=True)

    fig.savefig(h5file+'_activity.png', facecolor=fig.get_facecolor())

####################################################
#### collect and prepare data ######################
#### mark foodlocation for all videos if not present
# collect all project file names in Dataframe
projectfiles = pd.DataFrame({'videos': getvideos()})

# extract still frame
projectfiles['stillframes'] = ''
if len(projectfiles)>0:
    # check whether frame picture is there, otherwise generate it
    for video in projectfiles['videos']:
        if not os.path.isfile(video[:-4]+"_stillframe.png"):
            extractframe(video)
        projectfiles['stillframes'][projectfiles.index[projectfiles['videos'] == video]] = [video[:-4]+"_stillframe.png"]
else:
    print('no videos found')

# check whether there is a food file if not launch mark food app
projectfiles['foodcsvs'] = ''
for frame in projectfiles['stillframes']:
    if not os.path.isfile(frame+"food.csv"):
        getfoodlocation.startGUI(frame)
    projectfiles['foodcsvs'][projectfiles.index[projectfiles['stillframes'] == frame]] = [frame+"food.csv"]

# get list of h5 files corresponding to the videos
projectfiles['h5files'] = ''
for video in projectfiles['videos']:
    h5_file = glob.glob(video[:-4]+'*.h5')
    if h5_file:
        projectfiles['h5files'][projectfiles.index[projectfiles['videos'] == video]] = h5_file[0]



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

for h5file in projectfiles['h5files']:
    if h5file:
        foodcsv = projectfiles['foodcsvs'][projectfiles.index[projectfiles['h5files'] == h5file]].values[0]

        # feedingcount.feeding(h5file, csv of food cirlce, fps)
        animalsfeeding = analysis.feeding(h5file, foodcsv, 2)
        # feedingcount.feeding(h5file, fps)
        animalsactive = analysis.activity(h5file, 2)

        combined_df = pd.concat([animalsfeeding, animalsactive])
        #plotactivity graph
        plotactivity(h5file, combined_df, rollingwindow, starttime)
    else:
        print("no data to analyse for ", projectfiles['videos'][projectfiles.index[projectfiles['h5files'] == h5_file]][0])



##### frame videos for visualization of the process
import matplotlib.colors
import math

trail = 40

# colors
cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(vmin=-trail/2, vmax=0)

#image dimensions
import cv2
import csv
import numpy as np

RGBblack = (0,0,0)
RGBwhite = (255,255,255)

bgcolor = RGBblack

stillframe = projectfiles['stillframes'][projectfiles.index[projectfiles['h5files'] == h5file]][0]

image = cv2.imread(stillframe)
print(image.shape)
(im_height, im_width, color) = image.shape
image = np.zeros((im_height,im_width,color), np.uint8)
image[:,:]=bgcolor

df = animalsfeeding
df = df.iloc[:, df.columns.get_level_values(1).isin(['paemula3'])]

#df = df.iloc[:, (df.columns.get_level_values('bodyparts') == 'head') | (df.columns.get_level_values('bodyparts') == 'scutellum')]
df = df.iloc[:, (df.columns.get_level_values('bodyparts') == 'head')]


vidpath, vidname = os.path.split(os.path.abspath(projectfiles['videos'][projectfiles.index[projectfiles['h5files'] == h5_file]][0]))

# output video
vidout = cv2.VideoWriter('../data_vis/output/project_black.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 25, (im_width,im_height))

food = []
# get circle coordinates
if os.path.isfile(projectfiles['foodcsvs'][projectfiles.index[projectfiles['h5files'] == h5file]][0]):
    with open(projectfiles['foodcsvs'][projectfiles.index[projectfiles['h5files'] == h5file]][0], mode='r') as infile:
        file_reader = csv.reader(infile, delimiter=',', quotechar='"')
        # skip header
        next(file_reader)
        for row in file_reader:
            x,y,rad = row
            x,y,rad = int(x), int(y), int(rad)
            food += [[x,y,rad]]

feeding = []

df.columns = [col[3] for col in df.columns]
# black frames for the first frames in which the trail doesn't fit
for frame in range(trail):
    image[:,:]=bgcolor
    vidout.write(image)

for frame in range(trail, len(df)):
    image[:,:]=bgcolor

    for x,y,time in zip(list(df[frame-trail:frame]['x']),list(df[frame-trail:frame]['y']), [(x-max(list(df[frame-trail:frame].index)))/2 for x in list(df[frame-trail:frame].index)]):
        if not (math.isnan(x) & math.isnan(y)):
            x= int(x)
            y= int(y)
            # color by frame
            pointcolor=tuple([int(x*256) for x in cmap(norm(time))[:3]])
            image = cv2.circle(image, (x,y), radius=5, color=pointcolor, thickness=-1)

    ### skip a few for presentation vid
    if frame > 300:
        if (df['sumfeeding_0'][frame] == 1) | (df['sumfeeding_1'][frame] == 1):
            feeding += [[int(df['x'][frame]), int(df['y'][frame])]]


    # draw green circles for visits
    for coordinate in feeding:
        image = cv2.circle(image, tuple(coordinate), radius=5, color=(0,255,0), thickness=-1)

    #draw food circles
    image = cv2.circle(image, (food[0][0],food[0][1]), radius=food[0][2], color=RGBblack, thickness=2)
    image = cv2.circle(image, (food[1][0],food[1][1]), radius=food[1][2], color=RGBblack, thickness=2)

    vidout.write(image)

vidout.release()


# TODO
# presence at feed pots
#   duration of visit
# activity
#   resting vs moving
