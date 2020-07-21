import getfoodlocation.circularfood as markfood
from tkinter import Tk
from tkinter.filedialog import askdirectory
import glob
import os.path
import cv2

def getVideos():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    foldername = askdirectory() # show an "Open" dialog box and return the path to the selected file
    videos = glob.glob(os.path.join(foldername, '*.mp4'))
    return videos

def extractframe(video_name):

    vidObj = cv2.VideoCapture(video_name)

    if not vidObj.isOpened():
        print("could not open: ",video_name)
        return

    length = int(vidObj.get(cv2.CAP_PROP_POS_FRAMES))

    # get frame in the middle of the vid
    vidObj.set(2,round(length/2));
    ret, frame = vidObj.read()

    # Cut the video extension to have the name of the video
    my_video_name = video.split(".")[0]

    # save frame
    cv2.imwrite(my_video_name+'_stillframe.png', frame)

# mark foodlocation for all videos if not present
# get list of videos and extract still frame
videos = getVideos()
stillframes =[]
if videos:
    # check whether frame picture is there, otherwise generate it
    for video in videos:
        if not os.path.isfile(video[:-4]+"_stillframe.png"):
            extractframe(video)
        stillframes += [video[:-4]+"_stillframe.png"]
else:
    print('no videos found')

# check whether there is a food file if not launch mark foopd app
for frame in stillframes:
    if not os.path.isfile(frame+"food.csv"):
        markfood.startGUI(frame)

# get list of h5 files corresponding to the getVideos

# read in data and do something
