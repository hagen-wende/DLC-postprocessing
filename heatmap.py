import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial import cKDTree


def data_coord2view_coord(p, resolution, pmin, pmax):
    dp = pmax - pmin
    dv = (p - pmin) / dp * resolution
    return dv

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

path = "D:\\Hobby\\kaefer_tracking\\raspberry_pi\\00_DLC_postprocessing"
os.chdir(path)
Dataframe = pd.read_hdf(os.path.join("data","20200711_paemula_cropDLC_resnet50_200714PaemulaJul14shuffle1_50000_bx.h5"))

df = Dataframe.iloc[:, Dataframe.columns.get_level_values('bodyparts')=='scutellum']

xs=[]
ys=[]
xs=np.empty([1,])
ys=np.empty([1,])

for i, coordinates in enumerate(set(df.columns.get_level_values(1))):
    plot_df = df.iloc[:, df.columns.get_level_values(1)==coordinates]
    plot_df.columns = [col[3] for col in plot_df.columns]
    xs = np.concatenate([xs, plot_df.iloc[:,[0]]['x'].to_numpy()])
    ys = np.concatenate([ys, plot_df.iloc[:,[1]]['y'].to_numpy()])
    print("a")

# type(plot_df.iloc[:,[0]]['x'].to_numpy())
# n = 1000
# xs=xs+plot_df.iloc[:,[0]]['x'].to_numpy()
# xs=plot_df.iloc[:,[0]]['x'].to_numpy()
# ys=plot_df.iloc[:,[1]]['y'].to_numpy()
# len(xs)

n=1000
#remove NaNs
xs_new = xs[~np.isnan(xs)]
ys_new = ys[~np.isnan(xs)]
len(xs_new)
len(ys_new)
xs = xs_new[ys_new <2000]
ys = ys_new[ys_new <2000]
len(xs)
len(ys)

xs= xs[0:100000]
ys= ys[0:100000]
resolution = 250

extent = [np.min(xs), np.max(xs), np.min(ys), np.max(ys)]
xv = data_coord2view_coord(xs, resolution, extent[0], extent[1])
yv = data_coord2view_coord(ys, resolution, extent[2], extent[3])


def kNN2DDens(xv, yv, resolution, neighbours, dim=2):
    """
    """
    # Create the tree
    tree = cKDTree(np.array([xv, yv]).T)
    # Find the closest nnmax-1 neighbors (first entry is the point itself)
    grid = np.mgrid[0:resolution, 0:resolution].T.reshape(resolution**2, dim)
    dists = tree.query(grid, neighbours)
    # Inverse of the sum of distances to each grid point.
    inv_sum_dists = 1. / dists[0].sum(1)

    # Reshape
    im = inv_sum_dists.reshape(resolution, resolution)
    return im


fig, axes = plt.subplots(2, 2, figsize=(15, 15))
for ax, neighbours in zip(axes.flatten(), [0, 16, 32, 63]):

    if neighbours == 0:
        ax.plot(xs, ys, 'k.', markersize=5)
        ax.set_aspect('equal')
        ax.set_title("Scatter Plot")
    else:

        im = kNN2DDens(xv, yv, resolution, neighbours)

        ax.imshow(im, origin='lower', extent=extent, cmap=cm.Blues)
        ax.set_title("Smoothing over %d neighbours" % neighbours)
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])

plt.savefig('new.png', dpi=150, bbox_inches='tight')
