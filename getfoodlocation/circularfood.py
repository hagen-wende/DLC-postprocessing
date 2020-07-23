import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QHBoxLayout, QVBoxLayout, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter, QPen, QBrush
from PyQt5.QtCore import pyqtSlot, Qt
import cv2
import csv
import os

class Food_GUI(QWidget):

    def __init__(self, width, height, file):
        super().__init__()
        self.framewidth = width
        self.frameheight = height
        self.file = [file]
        self.radius = 60
        self.imgscalefact = 1
        self.initUI()
        if self.file[0] != '':
            self.show_image()
            self.textbox.setText(self.file[0])


    def initUI(self):
        self.resize(self.framewidth, self.frameheight) # frame size
        self.setWindowTitle('Foodsource Selector')
        self.setWindowIcon(QIcon("../icons/food.png"))

        # name for text vBox
        self.selectimg = QLabel("Select image", self)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.resize(400,20)

        # Create a button in the window
        self.browsebutton = QPushButton('Browse')

        # connect button to function on_click
        self.browsebutton.clicked.connect(self.browse)
        self.show()

        ### image
        self.labelImage = QLabel(self)
        self.pixmap = QPixmap(800,800)
        self.labelImage.setPixmap(self.pixmap)
        self.labelImage.mousePressEvent = self.getPixel

        # tools
        self.titel = QLabel('coordinates (scaled)')
        self.xcoordlabel = QLabel('x')
        self.ycoordlabel = QLabel('y')
        self.radiuslabel = QLabel('radius')
        self.xcoordtext = QLineEdit(self)
        self.xcoordtext.resize(100,20)
        self.ycoordtext = QLineEdit(self)
        self.ycoordtext.resize(100,20)
        self.radiustext = QLineEdit(self)
        self.radiustext.setText(str(self.radius))
        self.radiustext.returnPressed.connect(self.change_radius)

        self.savebutton = QPushButton('Save')
        self.savebutton.clicked.connect(self.savecoords)

        self.saveconfirmation = QLabel('')

    # img_label = QLabel()
    # img_label.setPixmap(pixmap)
    # img_label.mousePressEvent = self.getPixel


        #### Layout

        # file selection
        hBox = QHBoxLayout()
        hBox.addWidget(self.selectimg)
        hBox.addWidget(self.textbox)
        hBox.addWidget(self.browsebutton)

        # image
        hBox2 = QHBoxLayout()
        hBox2.addWidget(self.labelImage)

        # food Selector
        tools = QVBoxLayout()

        toolstitel = QHBoxLayout()
        toolstitel.addWidget(self.titel)

        toollabels = QHBoxLayout()
        toollabels.addWidget(self.xcoordlabel)
        toollabels.addWidget(self.ycoordlabel)
        toollabels.addWidget(self.radiuslabel)

        coordinates = QHBoxLayout()
        coordinates.addWidget(self.xcoordtext)
        coordinates.addWidget(self.ycoordtext)
        coordinates.addWidget(self.radiustext)

        savewidget = QHBoxLayout()
        savewidget.addWidget(self.savebutton)
        savewidget.addWidget(self.saveconfirmation)

        verticalSpacer = QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        tools.addItem(verticalSpacer)
        tools.addLayout(toolstitel)
        tools.addLayout(toollabels)
        tools.addLayout(coordinates)
        tools.addLayout(savewidget)

        verticalSpacer2 = QSpacerItem(0, 500, QSizePolicy.Minimum, QSizePolicy.Expanding)
        tools.addItem(verticalSpacer2)

        # main layout
        main = QVBoxLayout() # leere basis layout
        main.addLayout(hBox,1)

        bottom = QHBoxLayout()
        bottom.addLayout(hBox2,1)
        bottom.addLayout(tools,1)

        main.addLayout(bottom,1)

        self.setLayout(main) ## activate main
        self.show()



    def browse(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open file','.',"Image files (*.jpg *.gif *.png)")
        self.textbox.setText(self.file[0])
        self.show_image()

    def show_image(self):
        self.img = QImage(self.file[0])
        self.pixmap = QPixmap(QPixmap.fromImage(self.img))
        self.imgscalefact = self.pixmap.height()/800
        self.pixmap = self.pixmap.scaledToHeight(800)
        self.labelImage.setPixmap(self.pixmap)
        self.painter = QPainter(self.labelImage.pixmap())
        # draw circles for saved coordinates
        if os.path.isfile(self.file[0]+"food.csv"):
            with open(self.file[0]+"food.csv", mode='r') as infile:
                file_reader = csv.reader(infile, delimiter=',', quotechar='"')
                # skip header
                next(file_reader)
                for row in file_reader:
                    x,y,rad = row
                    x,y,rad = int(x)/self.imgscalefact, int(y)/self.imgscalefact, int(rad)/self.imgscalefact
                    x,y,rad = round(x), round(y), round(rad)
                    self.painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                    self.painter.drawEllipse(x-rad, y-rad, 2*rad, 2*rad)
        self.painter.end()


    def getPixel(self, event):
        self.xcoord = event.pos().x()
        self.ycoord = event.pos().y()
        self.xcoordtext.setText(str(self.xcoord))
        self.ycoordtext.setText(str(self.ycoord))
        self.saveconfirmation.setText('')
        self.draw_circle()

    def draw_circle(self):
        # reset painting area
        self.show_image()
        self.painter = QPainter(self.labelImage.pixmap())
        self.painter.setPen(QPen(Qt.green, 3, Qt.SolidLine))
        self.painter.drawEllipse(self.xcoord-self.radius, self.ycoord-self.radius, 2*self.radius, 2*self.radius)
        self.painter.end()
        self.update()

    def change_radius(self):
        self.radius = int(self.radiustext.text())
        self.draw_circle()

    def savecoords(self):
        # save coordinates and radius in csv
        if os.path.isfile(self.file[0]+"food.csv"):
            with open(self.file[0]+"food.csv", mode='a', newline='') as outfile:
                outfile_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                outfile_writer.writerow([round(self.xcoord*self.imgscalefact), round(self.ycoord*self.imgscalefact), round(self.radius*self.imgscalefact)])

        else:
            with open(self.file[0]+"food.csv", mode='w', newline='') as outfile:
                outfile_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                outfile_writer.writerow(['x', 'y', 'radius'])
                outfile_writer.writerow([round(self.xcoord*self.imgscalefact), round(self.ycoord*self.imgscalefact), round(self.radius*self.imgscalefact)])

        self.saveconfirmation.setText('coordinates saved')

def startGUI(file=''):
    # qapplication object
    app = QApplication(sys.argv)
    #### stylesheets
    app.setStyleSheet(STYLE)
    # actiate GUI with 800x800
    w = Food_GUI(800,800, file)
    # run the app
    app.exec_()


### stylesheets
STYLE = """
QLabel{
font-weight: bold;
color: black;
}
"""

if __name__ == '__main__':
    # qapplication object
    app = QApplication(sys.argv)
    #### stylesheets
    app.setStyleSheet(STYLE)
    # actiate GUI with 800x800
    w = Food_GUI(800,800, '')
    # run the app
    sys.exit(app.exec_())
