import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors


path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"

os.chdir(path)
Dataframe = pd.read_hdf(os.path.join("data","200711beetles_sample_sk.h5"))
#
# type(Dataframe)
# Dataframe.loc('scorer', axis=0)
# Dataframe.index
# Dataframe.to_csv('file_name.csv')
# df = Dataframe
#
# bodyparts=Dataframe.columns.get_level_values('bodyparts')
#
# df.loc[:, df.columns(2).isin(['scutellum'])]
#
# df[(df['bodyparts']=='Male') & (df['Year']==2014)]
#
# for individual in Dataframe['DLC_resnet50_Paemula Full DayJul10shuffle1_50000'].columns.get_level_values('individuals'):
#     print(individual)
#
#     df.drop(['A'], axis = 0)
#
# Dataframe['DLC_resnet50_Paemula Full DayJul10shuffle1_50000']['paemula1']['scutellum'].columns.get_level_values('coords')
# df =Dataframe['DLC_resnet50_Paemula Full DayJul10shuffle1_50000']['paemula1']
# df.drop(df.columns[[3,4]], axis = 1, inplace = True)
# [Dataframe.columns.get_level_values(1)]['scutellum']['likelihood'].values > pcutoff
#
# Dataframe.columns.get_level_values(2)
#
# Dataframe.columns['scutellum', axis=1, level=2]

df = Dataframe.iloc[:, Dataframe.columns.get_level_values(1)=='paemula5']
df = df.iloc[:, df.columns.get_level_values(2)=='scutellum']

df.columns = [col[3] for col in df.columns]

# pandas plot, but can't plot color gradient directly
# df.iloc[:,[0,1]].plot(x='x', y='y', legend=False, color=[(color,color,color) for color in df.index.values/np.max(df.index.values)])


# colors
cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(vmin=1, vmax=1600)

plt.scatter('x','y', data=df.iloc[:,[0,1]], color=cmap(norm(df.index.values)))
plt.show()
