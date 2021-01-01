import pandas as pd
import numpy as np
import os
import cv2
import time
import csv
import cython

def gauss():
    # Initializing value of x-axis and y-axis
    # in the range -1 to 1
    x, y = np.meshgrid(np.linspace(-10,10,51), np.linspace(-10,10,51))
    dst = np.sqrt(x*x+y*y)
    # Intializing sigma and muu
    sigma = 4
    muu = 0.000
    # Calculating Gaussian array
    gauss = np.exp(-( (dst-muu)**2 / ( 2.0 * sigma**2 ) ) )

    return gauss2D

### cython code needs to be implemented from jupyter notebook (this does not work yet)
@cython.boundscheck(False)
cpdef unsigned char[:, :] applygauss(heatmap, gauss, input_df):
    #for row in range(1,100):
    for row in range(len(input_df)):
        try:
            r, c = int(input_df['y'][row]+100)-24, int(input_df['x'][row]+100)-24
            heatmap[r:r+gauss.shape[0], c:c+gauss.shape[1]] += gauss
        except:
            pass
    return heatmap

def createheatmap(input_df, stillframe, foodcsv):

    animals = list(input_df.columns.levels[1])

    # load frame and get dimensions
    frame = cv2.imread(stillframe)
    height, width, channels = frame.shape

    # initialize empty heatmap
    heatmap = np.zeros(shape=[height+200, width+200], dtype=np.float)

    for animal in animals:
        print(animal,"start @ ", time.time()-jetzt, " seconds")
        heatmap = applygauss(heatmap,gauss,input_df[scorer][animal]['scutellum'])
        print(animal,"end   @ ", time.time()-jetzt, " seconds")

    # normalize heatmap
    Zmax, Zmin = heatmap.max(), heatmap.min()
    heatmap = ((heatmap-Zmin)/(Zmax-Zmin))*255
    heatmap = heatmap.astype(np.uint8)

    # custom color map (optional)
    owncolorMap = np.zeros((256,1,3))
    owncolorMap[:,0,1]=255
    for i,x in enumerate(range(256,-1,-1)):
        owncolorMap[i-1,0,0]=x
        owncolorMap[i-1,0,2]=x
    owncolorMap = owncolorMap.astype(np.uint8)

    # image needs to match LUT
    heatmapRGB = cv2.cvtColor(heatmap,cv2.COLOR_GRAY2RGB)

    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    #custom LUT
    #heatmap_color = cv2.LUT(heatmapRGB, owncolorMap)

    #mark the food sources
    with open(foodcsv) as infile:
        file_reader = csv.reader(infile, delimiter=',', quotechar='"')
        next(file_reader) # skip header
        for row in file_reader:
            x,y,rad,foodtype = row
            x,y,rad = int(x)+100, int(y)+100, int(rad)
            cv2.ellipse(heatmap_color, (x,y), (rad, rad), 0,0,360, (255,255,255), 3)

    # crop back to original image size
    heatmap_color = heatmap_color[100:height+100, 100:width+100]

    #save image
    cv2.imwrite(os.path.join(path,"data_testing_1",'heatmap_scutellum_crop.png'), heatmap_color)

    return

if __name__ == '__main__':
    # dataset for testing module
    path="D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"
    os.chdir(path)
    file = os.path.join(path,"data_testing_1","20200721_paemula_cropDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5")
    foodcsv = os.path.join(path,"data_testing_1","20200721_paemula_crop_stillframe.pngfood.csv")
    stillframe = os.path.join(path,"data_testing_1","20200721_paemula_crop_stillframe.png")

    input_df = pd.read_hdf(file)

    # we could also drop this level, since we are not using it
    scorer = input_df.columns[0][0]

    createheatmap(input_df, stillframe, foodcsv)

    plt.show()
