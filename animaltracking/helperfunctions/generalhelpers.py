import helperfunctions

import glob
import pandas as pd

def getprojectfiles():
    df_project = pd.DataFrame({'videos': helperfunctions.getvideos()})
    if df_project.empty:
        print("No video files found")
        return
    else:
        df_project['h5files'] = geth5files(df_project)
        if None in list(df_project['h5files']):
            return
        else:
            return df_project

def geth5files(df_project):
    if 'h5files' not in df_project.columns:
        df_project['h5files'] = ''

    for video in df_project['videos']:
        h5_file = glob.glob(video[:-4]+'*.h5')
        if h5_file:
            df_project['h5files'][df_project.index[df_project['videos'] == video]] = h5_file[0]
        else:
            print("No corresponding h5 file for ", video, "found!")
            return
    return df_project['h5files']

if __name__ == '__main__':
    ## do nothing
    print("General Helpers")
