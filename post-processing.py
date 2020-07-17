import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors


path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"

os.chdir(path)
Dataframe = pd.read_hdf(os.path.join("data","20200711_paemula_cropDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5"))
len(Dataframe)
Dataframe.index
animalsfeeding = pd.DataFrame(data= {'seconds': [], 'count': []})
animal ='paemula1'
line = 0

# only analyse head position
df_head = Dataframe.iloc[:, Dataframe.columns.get_level_values('bodyparts')=='head']

Dataframe['DLC_resnet50_200714PaemulaJul14shuffle1_50000']['paemula1']['head']['x'][0]

for line in range(len(Dataframe)):
    if Dataframe['DLC_resnet50_200714PaemulaJul14shuffle1_50000'][animal]['head']['x'][line] >400:
        print(line, ": ", Dataframe['DLC_resnet50_200714PaemulaJul14shuffle1_50000'][animal]['head']['x'][line])


    # for animal in set(df_head.columns.get_level_values('individuals')):
    #     df_animal = df_head.iloc[:, df_head.columns.get_level_values('individuals')==animal]
    #     df_animal.columns = [col[3] for col in df_animal.columns]
    #     if df_animal.loc[line, 'x'] > 400:
    #         print('yes')



# colors
cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(vmin=1, vmax=4)

image = plt.imread('data/img0259.png')
implot = plt.imshow(image)

#image dimensions
import cv2

im = cv2.imread('data/img0259.png')
print(im.shape)
(im_height, im_width, color) = im.shape


df = df.iloc[:, df.columns.get_level_values(1).isin(['paemula1'])]


df = Dataframe.iloc[:, Dataframe.columns.get_level_values('bodyparts')=='scutellum']

for i, coordinates in enumerate(set(df.columns.get_level_values(1))):
    plot_df = df.iloc[:, df.columns.get_level_values(1)==coordinates]
    plot_df.columns = [col[3] for col in plot_df.columns]
    # filter for likelihood
    #plot_df = plot_df[plot_df['likelihood']>0.99]
    # filtercoordinates
    # plot_df = plot_df[plot_df['x']>0]
    # plot_df = plot_df[plot_df['y']>0]
    # plot_df = plot_df[plot_df['x']<im_width]
    # plot_df = plot_df[plot_df['y']<im_height]
    # invert y
    #plot_df['y'] = -plot_df['y']
    # substract minx
    # plot_df['x'] = plot_df['x']-np.min(plot_df['x'])
    #plot_df = plot_df[plot_df['x']<1100]
    #invert x
    # plot_df['y'] = -plot_df['y']+np.max(plot_df['y'])
    plt.scatter('x','y', data=plot_df.iloc[:,[0,1]], color=cmap(norm(i+1)))

# put a red dot, size 40, at 2 locations: --> intersting for marking the jellys
plt.scatter(x=[30, 40], y=[50, 60], c='r', s=10)

plt.show()
