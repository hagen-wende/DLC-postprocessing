import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors


path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"

os.chdir(path)
Dataframe = pd.read_hdf(os.path.join("data","200711beetles_sample_sk.h5"))
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

for i, coordinates in enumerate(set(df.columns.get_level_values(1))):
    plot_df = df.iloc[:, df.columns.get_level_values(1)==coordinates]
    plot_df.columns = [col[3] for col in plot_df.columns]
    # filter for likelihood
    plot_df = plot_df[plot_df['likelihood']>0.95]
    # filtercoordinates
    plot_df = plot_df[plot_df['x']>0]
    plot_df = plot_df[plot_df['y']>0]
    # invert y
    #plot_df['y'] = -plot_df['y']
    # substract minx
    plot_df['x'] = plot_df['x']-np.min(plot_df['x'])
    plt.scatter('x','y', data=plot_df.iloc[:,[0,1]], color=cmap(norm(i+1)))

plt.show()
