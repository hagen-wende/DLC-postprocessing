### ToDo ...
### tracking video code, needs to be refined and put into a module
##### frame videos for visualization of the process
import matplotlib.colors
import math

trail = 40

# colors
cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(vmin=-trail/2, vmax=0)

#image dimensions
import cv2
import csv
import numpy as np

RGBblack = (0,0,0)
RGBwhite = (255,255,255)
RGBbggrey =(227,225,227)

bgcolor = RGBbggrey

stillframe = projectfiles['stillframes'][projectfiles.index[projectfiles['h5files'] == h5file]][0]

image = cv2.imread(stillframe)
print(image.shape)
(im_height, im_width, color) = image.shape
image = np.zeros((im_height,im_width,color), np.uint8)
image[:,:]=bgcolor

df = animalsfeeding
df = df.iloc[:, df.columns.get_level_values(1).isin(['paemula3'])]

#df = df.iloc[:, (df.columns.get_level_values('bodyparts') == 'head') | (df.columns.get_level_values('bodyparts') == 'scutellum')]
df = df.iloc[:, (df.columns.get_level_values('bodyparts') == 'head')]


vidpath, vidname = os.path.split(os.path.abspath(projectfiles['videos'][projectfiles.index[projectfiles['h5files'] == h5_file]][0]))

# output video
vidout = cv2.VideoWriter('../data_vis/output/project_white.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 25, (im_width,im_height))

food = []
# get circle coordinates
if os.path.isfile(projectfiles['foodcsvs'][projectfiles.index[projectfiles['h5files'] == h5file]][0]):
    with open(projectfiles['foodcsvs'][projectfiles.index[projectfiles['h5files'] == h5file]][0], mode='r') as infile:
        file_reader = csv.reader(infile, delimiter=',', quotechar='"')
        # skip header
        next(file_reader)
        for row in file_reader:
            x,y,rad = row
            x,y,rad = int(x), int(y), int(rad)
            food += [[x,y,rad]]

feeding = []

df.columns = [col[3] for col in df.columns]
# black frames for the first frames in which the trail doesn't fit
for frame in range(trail):
    image[:,:]=bgcolor
    vidout.write(image)

for frame in range(trail, len(df)):
    image[:,:]=bgcolor

    for x,y,time in zip(list(df[frame-trail:frame]['x']),list(df[frame-trail:frame]['y']), [(x-max(list(df[frame-trail:frame].index)))/2 for x in list(df[frame-trail:frame].index)]):
        if not (math.isnan(x) & math.isnan(y)):
            x= int(x)
            y= int(y)
            # color by frame
            pointcolor=tuple([int(x*256) for x in cmap(norm(time))[:3]])
            image = cv2.circle(image, (x,y), radius=5, color=pointcolor, thickness=-1)

    ### skip a few for presentation vid
    if frame > 300:
        if (df['sumfeeding_0'][frame] == 1) | (df['sumfeeding_1'][frame] == 1):
            feeding += [[int(df['x'][frame]), int(df['y'][frame])]]


    # draw green circles for visits
    for coordinate in feeding:
        image = cv2.circle(image, tuple(coordinate), radius=5, color=(0,255,0), thickness=-1)

    #draw food circles
    image = cv2.circle(image, (food[0][0],food[0][1]), radius=food[0][2], color=RGBblack, thickness=2)
    image = cv2.circle(image, (food[1][0],food[1][1]), radius=food[1][2], color=RGBblack, thickness=2)

    vidout.write(image)

vidout.release()
