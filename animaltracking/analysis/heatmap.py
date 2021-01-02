import pandas as pd
import numpy as np
import os
import cv2
import csv

def gauss(size):
    # Intializing sigma and muu
    # sigma was choosen so that the linspace falls off to almost zero towards the sides
    sigma = 4
    muu = 0.000

    # Initializing value of x-axis and y-axis
    x, y = np.meshgrid(np.linspace(-(2*sigma+2),2*sigma+2,size), np.linspace(-(2*sigma+2),2*sigma+2,size))
    dst = np.sqrt(x*x+y*y)

    # Calculating Gaussian array
    gauss2D = np.exp(-( (dst-muu)**2 / ( 2.0 * sigma**2 ) ) )

    return gauss2D

def applygauss(heatmap, gauss, input_df):

    for row in range(len(input_df)):
        try:
            # koordinate + offset for addional space around the image (gauss.shape[0]*2)
            # minus half of the gauss2D distribution, to have the center at the koordinate
            r, c = int(np.around(input_df['y'][row]+gauss.shape[0]*2-(gauss.shape[0]-1)/2)), int(np.around(input_df['x'][row]+gauss.shape[0]*2-(gauss.shape[0]-1)/2))
            heatmap[r:r+gauss.shape[0], c:c+gauss.shape[1]] += gauss
        except:
            # NaNs and  strange x,y values are ignored
            pass
    return heatmap

    # custom color map (optional)
def customColormap():
    # custom colors not implemented
    # this gives gradient from white to green
    owncolorMap = np.zeros((256,1,3))
    owncolorMap[:,0,1]=255
    for i,x in enumerate(range(256,-1,-1)):
        owncolorMap[i-1,0,0]=x
        owncolorMap[i-1,0,2]=x
    owncolorMap = owncolorMap.astype(np.uint8)

def createheatmap(h5file, df_project, bodypart, gausssize=51):

    input_df = pd.read_hdf(h5file)
    stillframe = df_project.at[df_project.index[df_project['h5files'] == h5file][0],'stillframes']
    scorer =input_df.columns[0][0]

    #size of the 2Dgauss must be uneven to have a center
    if gausssize % 2 == 0:
        gausssize=gausssize+1

    animals = list(input_df.columns.levels[1])

    # load frame and get dimensions
    frame = cv2.imread(stillframe)
    height, width, channels = frame.shape

    # initialize empty heatmap with additional space for points at the edges
    heatmap = np.zeros(shape=[height+gausssize*4, width+gausssize*4], dtype=np.float)
    print("Creating heatmap ... ")
    for animal in animals:
        print(animal)
        heatmap = applygauss(heatmap,gauss(gausssize),input_df[scorer][animal][bodypart])

    # normalize heatmap
    Zmax, Zmin = heatmap.max(), heatmap.min()
    heatmap = ((heatmap-Zmin)/(Zmax-Zmin))*255
    heatmap = heatmap.astype(np.uint8)

    # apply color palette
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # custom LUT
    # image needs to match LUT
    # heatmapRGB = cv2.cvtColor(heatmap,cv2.COLOR_GRAY2RGB)
    # heatmap_color = cv2.LUT(heatmapRGB, customColormap())


    # crop back to original image size
    heatmap_color = heatmap_color[gausssize*2:height+gausssize*2, gausssize*2:width+gausssize*2]

    return heatmap_color

def saveheatmapwithfood(heatmap_color, h5file, df_project, bodypart):

    foodcsv = df_project.at[df_project.index[df_project['h5files'] == h5file][0],'foodcsvs']
    #mark the food sources
    with open(foodcsv) as infile:
        file_reader = csv.reader(infile, delimiter=',', quotechar='"')
        next(file_reader) # skip header
        for row in file_reader:
            x,y,rad,foodtype = row
            x,y,rad = int(x), int(y), int(rad)
            cv2.ellipse(heatmap_color, (x, y), (rad, rad), 0,0,360, (255,255,255), 3)

    # get base path from foodcsv
    path = foodcsv.rsplit('still',1)[0]

    #save image
    cv2.imwrite(path+'heatmap_'+bodypart+'_crop.png', heatmap_color)


if __name__ == '__main__':
    # dataset for testing module
    path="D:/Hobby/kaefer_tracking/raspberry_pi/00_DLC_postprocessing/data_testing_1"
    os.chdir(path)
    file = os.path.join(path,"20200721_paemula_cropDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5")
    df_project = pd.read_csv(os.path.join(path,"project_df.csv"))

    bodypart = 'head'

    # a good value for gausssize is 1/20th of the frame height/width. maller size gives sharper distribution, larger size more blurred distrinbution
    heatmap = createheatmap(file, df_project, bodypart, 51)
    saveheatmapwithfood(heatmap, file, df_project,bodypart)
