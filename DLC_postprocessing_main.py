import getfoodlocation.circularfood as markfood
import analysis.feedingcount as feedingcount
from tkinter import Tk
from tkinter.filedialog import askdirectory
import glob
import os.path
import cv2
import pandas as pd
import matplotlib.pyplot as plt

def getvideos():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    foldername = askdirectory() # show an "Open" dialog box and return the path to the selected file
    videos = glob.glob(os.path.join(foldername, '*.mp4'))
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

# mark foodlocation for all videos if not present
# get list of videos and extract still frame
# collect all project file names in Dataframe
projectfiles = pd.DataFrame({'videos': getvideos()})
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
        markfood.startGUI(frame)
    projectfiles['foodcsvs'][projectfiles.index[projectfiles['stillframes'] == frame]] = [frame+"food.csv"]

# get list of h5 files corresponding to the videos
projectfiles['h5files'] = ''
for video in projectfiles['videos']:
    h5_file = glob.glob(video[:-4]+'*.h5')
    if h5_file:
        projectfiles['h5files'][projectfiles.index[projectfiles['videos'] == video]] = h5_file[0]

# Analysis
# general activity
#   number of animals active
# presence at feed pots
#   total
#   comparison between different food sources

for h5file in projectfiles['h5files']:
    if h5file:
        foodcsv = projectfiles['foodcsvs'][projectfiles.index[projectfiles['h5files'] == h5file]][0]
        # for small files rollingwindow must be reduced!!!
        animalsfeeding = feedingcount.analysis(h5file, foodcsv, 2, 100)
        print(h5file)
    else:
        print("no data to analyse for ", projectfiles['videos'][projectfiles.index[projectfiles['h5files'] == h5_file]][0])

animalsfeeding[animalsfeeding.columns[0][0],'all','analysis'].plot(x='time')
plt.show()
# make rollig mean to smooth dataframe
input_df[input_df.columns[0][0],'all','analysis','sumfeeding_'+str(i)] = input_df[input_df.columns[0][0],'all','analysis','sumfeeding_'+str(i)].rolling(rollingwindow).mean()
input_df[input_df.columns[0][0],'all','analysis','isactive'] = input_df[input_df.columns[0][0],'all','analysis','isactive'].rolling(rollingwindow).mean()
# TODO
# presence at feed pots
#   duration of visit
