import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors


path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"

os.chdir(path)
Dataframe = pd.read_hdf(os.path.join("data","200711beetles_sample_sk.h5"))
#

df = Dataframe.iloc[:, Dataframe.columns.get_level_values(1)=='paemula8']
df = df.iloc[:, df.columns.get_level_values(2)=='scutellum']
df = Dataframe.iloc[:, Dataframe.columns.get_level_values(2)=='scutellum']

df.plot(legend=False)
df.columns = [col[3] for col in df.columns]

# colors
cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(vmin=1, vmax=8)

plt.scatter('x','y', data=df.iloc[:,[0,1]], color=cmap(norm(df.index.values)))
for i, coordinates in enumerate(set(df.columns.get_level_values(1))):
    df.iloc[:, df.columns.get_level_values(1)==coordinates]
    plt.scatter('x','y', data=df.iloc[:, df.columns.get_level_values(1)==coordinates].iloc[:,[0,1]], color=cmap(norm(i)))

plt.hist('x',data=df.iloc[:,[0]])

#plt.show()
