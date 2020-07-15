import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors


path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"

os.chdir(path)
Dataframe = pd.read_hdf(os.path.join("data","200710_paemula_crop_sampleDLC_resnet50_200714PaemulaJul14shuffle1_50000_sk.h5"))
#

# df = Dataframe.iloc[:, Dataframe.columns.get_level_values(1)=='paemula8']
# df = df.iloc[:, df.columns.get_level_values(2)=='scutellum']
df = Dataframe.iloc[:, Dataframe.columns.get_level_values(2)=='scutellum']

# df.plot(legend=False)
# df.columns = [col[3] for col in df.columns]

# colors
cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(vmin=1, vmax=4)

# filter df for first 4 individuals
df = df.iloc[:, df.columns.get_level_values(1).isin(['paemula1', 'paemula2', 'paemula3','paemula4'])]


image = plt.imread('data/img0259.png')
implot = plt.imshow(image)

#image dimensions

import cv2

im = cv2.imread('data/img0259.png')

print(im.shape)

(im_height, im_width, color) = im.shape

for i, coordinates in enumerate(set(df.columns.get_level_values(1))):
    plot_df = df.iloc[:, df.columns.get_level_values(1)==coordinates]
    plot_df.columns = [col[3] for col in plot_df.columns]
    # filter for likelihood
    plot_df = plot_df[plot_df['likelihood']>0.99]
    # filtercoordinates
    plot_df = plot_df[plot_df['x']>0]
    plot_df = plot_df[plot_df['y']>0]
    plot_df = plot_df[plot_df['x']<im_width]
    plot_df = plot_df[plot_df['y']<im_height]
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
