file = path+"\\data\\img0259.pngfood.csv"
animalsfeeding = pd.DataFrame(index=Dataframe.index.values, columns=['time', 'sumfeeding'])
animalsfeeding['time'] = [x / (180*60) for x in list(animalsfeeding.index)]
animalsfeeding['sumfeeding'] = 0

if os.path.isfile(file):
    with open(file, mode='r') as infile:
        file_reader = csv.reader(infile, delimiter=',', quotechar='"')
        # skip header
        next(file_reader)
        for line in file_reader:
            x_food,y_food,rad_food = line
            for animal in set(Dataframe.columns.get_level_values('individuals')):
                animalsfeeding['sumfeeding'] += Dataframe['DLC_resnet50_200714PaemulaJul14shuffle1_50000'][animal]['head'].apply(lambda row: incircle(row['x'], row['y'], x_food, y_food, rad_food), axis=1)
