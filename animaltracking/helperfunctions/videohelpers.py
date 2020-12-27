from tkinter import Tk
from tkinter.filedialog import askdirectory
import glob
import os.path
import cv2

def getvideos():
    root = Tk()
    root.wm_attributes('-topmost', 1) # opens windows in front
    # root.withdraw() # we don't want a full GUI, so keep the root window from appearing --> file select window is not scaleable
    foldername = askdirectory() # show an "Open" dialog box and return the path to the selected file
    videos = glob.glob(os.path.join(foldername, '*.mp4'))
    root.destroy()
    return videos

def extractframes(df_project):
        # check whether frame picture is there, otherwise generate it
    if len(df_project)>0:

        if 'stillframes' not in df_project.columns:
            df_project['stillframes'] = ''

        for video in df_project['videos']:
            if not os.path.isfile(video[:-4]+"_stillframe.png"):
                vidObj = cv2.VideoCapture(video)

                if not vidObj.isOpened():
                    print("could not open: ", video)
                    return

                # get number of frames of the video
                length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))

                # get frame in the middle of the vid
                vidObj.set(cv2.CAP_PROP_POS_FRAMES,round(length/2));
                ret, frame = vidObj.read()

                # Cut the video extension to have the name of the video
                my_video_name = video.split(".")[0]

                # save frame as png
                cv2.imwrite(my_video_name+'_stillframe.png', frame)

            # add name of stillframe to project
            df_project['stillframes'][df_project.index[df_project['videos'] == video]] = [video[:-4]+"_stillframe.png"]

        return df_project['stillframes']
    else:
        print('no videos found')



if __name__ == '__main__':
    ## do nothing
    print("Videohelpers")
