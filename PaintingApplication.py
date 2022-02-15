# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# NB If the menus do not work then click on another application ad then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

#  PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

import sys
from enum import Enum
from PyQt5.QtGui import QIcon, QImage, QPen, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QGridLayout, QAction, QGroupBox, QRadioButton, QSlider, \
    QLabel, QPushButton, QApplication, QFileDialog, QColorDialog, QMessageBox
from PyQt5.QtCore import Qt, QPoint, QSize
from qtpy import QtCore, QtGui


class PaintingApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting some settings of the window e.g. size, name and icon.
        self.setWindowTitle("Paint Application")
        self.setGeometry(200, 200, 900, 700)  # top, left, width, height
        self.setWindowIcon(QIcon("icon/back.jpeg"))

        # Layouts are initialized, and methods to initialize specific parts of the window are called.
        self.grid = QGridLayout()
        self.box = Toolkit()
        self.setPaintStyle()
        self.setPaintCap()
        self.setPaintJoin()
        self.PaintColorChnager()
        self.drawing = PaintArea()
        self.setPaintSlider()

        # Creates a grid using the Toolkit.
        # which are both placed in a widget.
        self.grid.addWidget(self.box, 0, 0, 1, 1)
        self.grid.addWidget(self.drawing, 0, 1, 1, 6)
        number = QWidget()
        number.setLayout(self.grid)
        self.setCentralWidget(number)

        # Creates three menus in our window's menu bar.
        # menus
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(" File")  # the space is required as the "File" is reserved in Mac.
        typeMenu = mainMenu.addMenu("Brush Type")
        helpMenu = mainMenu.addMenu("Help")
        # The Save action is created and added to the "File" menu.
        saveAction = QAction(QIcon('icon/save.png'), "Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        # The save action is triggered when the menu option is selected or the shortcut is utilized.
        saveAction.triggered.connect(self.save)

        # The Open action is created and added to the "File" menu.
        openAction = QAction(QIcon('icon/open.png'), "Open", self)
        openAction.setShortcut("Ctrl+O")
        fileMenu.addAction(openAction)
        # The open action is triggered when the menu option is selected or the shortcut is utilized.
        openAction.triggered.connect(self.open)
        # The Undo action is created and added to the "File" menu.
        undoAction = QAction(QIcon('icon/undo.png'), "Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        fileMenu.addAction(undoAction)
        # The undo action is triggered when the menu option is selected or the shortcut is utilized.
        undoAction.triggered.connect(self.undo)

        # The Clear action is created and added to the "File" menu.
        clearAction = QAction(QIcon('icon/clear.png'), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        # The clear action is triggered when the menu option is selected or the shortcut is utilized.
        clearAction.triggered.connect(self.clear)

        # Exit action is created and added to the "File" menu.
        exitAction = QAction(QIcon('icon/exit.png'), "Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        fileMenu.addAction(exitAction)
        # The exit action is triggered when the menu option is selected or the shortcut is used.
        exitAction.triggered.connect(self.exitProgram)
        # The StartPoint action is created and added to the "Brush Type" menu.
        self.StartPointAction = QAction("Start Point", self, checkable=True)
        self.StartPointAction.setShortcut("Ctrl+P")
        self.StartPointAction.setChecked(True)
        typeMenu.addAction(self.StartPointAction)
        # The change Paint action is initiated when the menu option is selected.
        self.StartPointAction.triggered.connect(lambda: self.drawType(self.StartPointAction))
        # The Line action is created and added to the "Brush Type" menu.
        self.lineAction = QAction("Line", self, checkable=True)
        self.lineAction.setShortcut("Ctrl+L")
        typeMenu.addAction(self.lineAction)
        # The change Paint action is initiated when the menu item is selected or the shortcut is utilized.
        self.lineAction.triggered.connect(lambda: self.drawType(self.lineAction))

        # The About action is created and added to the "Help" menu.
        aboutAction = QAction(QIcon('icon/art.png'), "About", self)
        aboutAction.setShortcut("Ctrl+I")
        helpMenu.addAction(aboutAction)
        # The about action is initiated when the menu option is selected or the shortcut is utilized.
        aboutAction.triggered.connect(self.about)

        # The Help action is created and added to the "Help" menu.
        helpAction = QAction(QIcon('icon/help.png'), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        # The help action is triggered when the menu option is selected or the shortcut is utilized.
        helpAction.triggered.connect(self.help)

        # The widget is updated with the default settings.
        self.drawing.update()

# The Paint is changed based on which action has been called.
    def drawType(self, check):
        if check.text() == "Start Point":
            self.StartPointAction.setChecked(True)
            self.lineAction.setChecked(False)
            self.drawing.Paint = Paint.StartPoint
        elif check.text() == "Line":
            self.StartPointAction.setChecked(False)
            self.lineAction.setChecked(True)
            self.drawing.Paint = Paint.Line
        # Resetting the saved StartPoint.
        self.drawing.lastPoint = QPoint()

        # Sets up the arrangement for adjusting the Join setting of the brush.
    def setPaintJoin(self):
        self.paint_join_style = QGroupBox("Brush Join")
        self.paint_join_style.setMaximumHeight(150)

        # The radio buttons were designed to allow us to select one of these three options.
        # Each one has a mechanism that changes the setting depending on which button is pressed.
        self.joinBtn1 = QRadioButton("Bevel")
        self.joinBtn1.clicked.connect(lambda: self.changePaintJoin(self.joinBtn1))
        self.joinBtn2 = QRadioButton("Round")
        self.joinBtn2.clicked.connect(lambda: self.changePaintJoin(self.joinBtn2))
        self.joinBtn3 = QRadioButton("Miter")
        self.joinBtn3.clicked.connect(lambda: self.changePaintJoin(self.joinBtn3))

        # Establishes a default value.
        # The layout is added to the parent box, and the buttons are added to the layout.
        self.joinBtn1.setChecked(True)
        qv = QVBoxLayout()
        qv.addWidget(self.joinBtn1)
        qv.addWidget(self.joinBtn2)
        qv.addWidget(self.joinBtn3)
        self.paint_join_style.setLayout(qv)
        self.box.vbox.addWidget(self.paint_join_style)

    # Sets up the layout on which we can adjust the brush's Type setting.
    def setPaintStyle (self):
        self.paint_line_style = QGroupBox("Brush style")
        self.paint_line_style.setMaximumHeight(150)
        # Creates the radio buttons so that we can choose amongst the three options.
        #  Each one has a mechanism that changes the setting depending on which button is pressed.
        self.SButton1 = QRadioButton(" Solid")
        self.SButton1.setIcon(QIcon('icon/solid.png'))
        self.SButton1.setIconSize(QSize(34, 65))
        self.SButton1.clicked.connect(lambda: self.changePaintStyle(self.SButton1))

        self.SButton2 = QRadioButton(" Dash")
        self.SButton2.setIcon(QIcon('icon/dash.png'))
        self.SButton2.setIconSize(QSize(34, 65))
        self.SButton2.clicked.connect(lambda: self.changePaintStyle(self.SButton2))

        self.SButton3 = QRadioButton(" Dot")
        self.SButton3.setIcon(QIcon('icon/dot.png'))
        self.SButton3.setIconSize(QSize(34, 65))
        self.SButton3.clicked.connect(lambda: self.changePaintStyle(self.SButton3))

        # Set a default value.
        # The layout is added to the parent box, and the buttons are added to the layout.
        self.SButton1.setChecked(True)
        qv = QVBoxLayout()
        qv.addWidget(self.SButton1)
        qv.addWidget(self.SButton2)
        qv.addWidget(self.SButton3)
        self.paint_line_style.setLayout(qv)
        self.box.vbox.addWidget(self.paint_line_style)

    # Sets up the layout on which we can adjust the brush's Cap setting.
    # Each one is linked to a method that alters the setting based on which button is pressed.
    def setPaintCap(self):
        self.Paint_cap_style = QGroupBox("Brush cap")
        self.Paint_cap_style.setMaximumHeight(150)

        # Creates the radio buttons so that we can select one of these three possibilities.
        self.CButton1 = QRadioButton("Flat")
        self.CButton1.setIcon(QIcon('icon/flat.png'))
        self.CButton1.clicked.connect(lambda: self.changePaintCap(self.CButton1))
        self.CButton2 = QRadioButton("Round")
        self.CButton2.setIcon(QIcon('icon/circle.png'))
        self.CButton2.clicked.connect(lambda: self.changePaintCap(self.CButton2))
        self.CButton3 = QRadioButton("Square")
        self.CButton3.setIcon(QIcon('icon/square.png'))
        self.CButton3.clicked.connect(lambda: self.changePaintCap(self.CButton3))

        # Establishes a default value.
        # The layout is added to the parent box, and the buttons are added to the layout.
        self.CButton3.setChecked(True)
        qv = QVBoxLayout()
        qv.addWidget(self.CButton1)
        qv.addWidget(self.CButton2)
        qv.addWidget(self.CButton3)
        self.Paint_cap_style.setLayout(qv)
        self.box.vbox.addWidget(self.Paint_cap_style)

    # Creates the radio buttons so that we can choose amongst the three options.
    # Each one has a method that changes the setting depending on which button is pressed.

    # This method modifies the brush's Cap setting depending on which button was previously pressed.
    def changePaintCap(self, button):
        if button.text() == "Flat":
            if button.isChecked():
                self.drawing.brushCap = Qt.FlatCap
        if button.text() == "Square":
            if button.isChecked():
                self.drawing.brushCap = Qt.SquareCap
        if button.text() == "Round":
            if button.isChecked():
                self.drawing.brushCap = Qt.RoundCap

    # This method changes the brush's Type setting depending on whichever button was previously pressed.
    def changePaintStyle(self, button):
        if button.text() == " Dash":
            if button.isChecked():
                self.drawing.brushStyle = Qt.DashLine
        if button.text() == " Solid":
            if button.isChecked():
                self.drawing.brushStyle = Qt.SolidLine
        if button.text() == " Dot":
            if button.isChecked():
                self.drawing.brushStyle = Qt.DotLine

    def changePaintJoin(self, button):
        if button.text() == "Miter":
            if button.isChecked():
                self.drawing.brushJoin = Qt.MiterJoin
        if button.text() == "Round":
            if button.isChecked():
                self.drawing.brushJoin = Qt.RoundJoin
        if button.text() == "Bevel":
            if button.isChecked():
                self.drawing.brushJoin = Qt.BevelJoin

    # Sets up the arrangement so that we can adjust the brush size.
    def setPaintSlider(self):
        self.groupBoxSlider = QGroupBox("Brush size")
        self.groupBoxSlider.setMaximumHeight(150)

        # Setting  a vertical slider with a min and a max value.
        self.paint_thickness = QSlider(Qt.Horizontal)
        self.paint_thickness.setMinimum(2)
        self.paint_thickness.setMaximum(50)
        self.paint_thickness.valueChanged.connect(self.changePaintSlider)

        #  Setting a label to display the size of the brush.
        self.paintSizeLabel = QLabel()
        self.paintSizeLabel.setText("%1s px" % self.drawing.brushSize)

        # Adding the buttons to the layout which is added to the parent box.
        qv = QVBoxLayout()
        qv.addWidget(self.paint_thickness)
        qv.addWidget(self.paintSizeLabel)
        self.groupBoxSlider.setLayout(qv)

        self.box.vbox.addWidget(self.groupBoxSlider)

    # The brush size is changed based on the value given by the slider in this method.
    def changePaintSlider(self, value):
        self.drawing.brushSize = value
        self.paintSizeLabel.setText("%s px" % value)

    # Sets up the layout on which we can adjust the brush's color.
    def PaintColorChnager(self):
        self.Paint_box_colour = QGroupBox("Color")
        self.Paint_box_colour.setMaximumHeight(150)

       # Sets the background color of a button to the initial color.

        self.paint_colour = QPushButton()
        self.paint_colour.setFixedSize(95, 95)
        self.paint_colour.clicked.connect(self.showPaintColorDialog)
        self.box.vbox.addWidget(self.paint_colour)

        # Adding the buttons to the layout which is added to the parent box.
        qv = QVBoxLayout()
        qv.addWidget(self.paint_colour)
        self.Paint_box_colour.setLayout(qv)

        self.box.vbox.addWidget(self.Paint_box_colour)

    # Displays a color picker and changes the color of the brush.
    def showPaintColorDialog(self):
        self.colour = QColorDialog.getColor()
        if self.colour.isValid():
            self.paint_colour.setStyleSheet("background-color: %s" % self.colour.name())
            self.drawing.brushColor = self.colour

    # When the main window is resized, this method is invoked.
    # resize event - this fuction is called
    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if self.drawing.resizeSavedImage.width() != 0:
            self.drawing.image = self.drawing.resizeSavedImage.scaled(self.drawing.width(), self.drawing.height(), QtCore.Qt.IgnoreAspectRatio)
        self.drawing.update()
    # slots

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.drawing.image.save(filePath)

        """
        When we run the open action, this method is invoked. 
        It brings up a file dialog box where the user can select the image's path to open in the software.
        """

    def open(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":
            return
        with open(filePath, 'rb') as f:
            content = f.read()

            """
            The data from the file is loaded into the image. 
            It is scaled and the drawing area is updated.
            """
            self.drawing.image.loadFromData(content)
            self.drawing.image = self.drawing.image.scaled(self.drawing.width(), self.drawing.height(),
                                                               QtCore.Qt.IgnoreAspectRatio)
            self.drawing.resizeSavedImage = self.drawing.image  # saves the image for later resizing
            self.drawing.update()

        """
        When we perform an undo action, this method is invoked. 
        The user can restore the image to its previous state prior to the last update he made.
        """

    def undo(self):
        copyImage = self.drawing.image
        if self.drawing.savedImage.width() != 0:
            # If the saved image exists, we use it as the actual image, scaled to the appropriate size.
                self.drawing.image = self.drawing.savedImage.scaled(self.drawing.width(), self.drawing.height(), QtCore.Qt.IgnoreAspectRatio)
        else:
            # We simply clean the current picture if no saved image exists.
            self.drawing.image = QImage(self.drawing.width(), self.drawing.height(), QImage.Format_RGB32)
            self.drawing.image.fill(Qt.white)
            # Sets the saved image as the screen's duplicate.
            self.drawing.savedImage = copyImage
            self.drawing.update()

        # When we execute the clear action, the method is invoked.
        # It updates the image by filling it with white.
    def clear(self):
        self.drawing.image.fill(Qt.white)
        self.drawing.update()
        # call the update method of the widget which calls the paintEvent of this class

    def exitProgram(self):
        QtCore.QCoreApplication.quit()

    # When the about action is performed, the method is invoked.
    # A notice regarding the software is displayed.
    def about(self):
        QMessageBox.about(self, "About QPaint",
                      "<p>Qt Application is a basic paint program made with PyQt. "
                      "You can draw something by yourself and then save it as a file. "
                      "PNG JPEG and JPG files can also be opened and edited.</p>")

    #  Method called when we execute the help action.
    #     Displays a help message about the program.
    def help(self):
        msg = QMessageBox()
        msg.setText("Help"
                "<p>Welcome to QPaint.</p> "
                "<p>On the left side of the screen, you'll notice a toolkit with many components. "
                "Each part will have a button or slider that you can use to customize the brush you want to draw with.</p>"
                "<p>The drawing area, which is the right size of the screen, is where you can draw..</p> "
                "<pThe program also contains numerous menus at the top of the window that you can see. " "p> You may use these choices to open a file, save it, clean it, and even exit the software. </p> " "We wish you a pleasant experience.")
        msg.setWindowTitle("Help")
        msg.move(self.width() / 2, self.height() / 2)
        msg.exec_()


# Defines an enum which represents the Painting modes.
class Paint(Enum):
    StartPoint = 1
    Line = 2


# Class inherited from a QWidget which initializes the Toolkit on the left of the application.
class Toolkit(QWidget):
    def __init__(self):
        super().__init__()

        # Setting a fix width.
        self.setMaximumWidth(150)
        self.setMinimumWidth(150)

        # Setting a vertical box layout
        # setting as the default layout.
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)


# Class inherited from a QWidget.
class PaintArea(QWidget):
    def __init__(self):
        super().__init__()

        # Initializing the two images
        # It will be used later to resize or undo.
        self.resizeSavedImage = QImage(0, 0, QImage.Format_RGB32)
        self.savedImage = QImage(0, 0, QImage.Format_RGB32)

        # Sets our default image with the right size filled in white.
        self.image = QImage(self.width(), self.height(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        # Setting the paint settings. e.g.Colour, Brush Style and Brush size
        self.drawing = False
        self.brushSize = 1
        self.brushColor = Qt.black
        self.brushStyle = Qt.SolidLine
        self.brushCap = Qt.RoundCap
        self.brushJoin = Qt.RoundJoin
        self.Paint = Paint.StartPoint

        # Setting a minimum width.
        self.lastPoint = QPoint()
        self.setMinimumWidth(150)

    """
    Method is being called.
    The image needs to be scaled with the new size or else problem could occur.
    """
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # Method is being called when a button of the mouse is pressed.
    def mousePressEvent(self, event):              # when the mouse is pressed, documentation: https://doc.qt.io/qt-5/qwidget.html#mousePressEvent
        if event.button() == Qt.LeftButton:  # if the pressed button is the left button
            if self.Paint == Paint.StartPoint:
                painter = QPainter(self.image)
                painter.drawPoint(event.pos())
                painter.setPen(QPen(self.brushColor, self.brushSize, self.brushStyle, self.brushCap, self.brushJoin))
                self.drawing = True             # drawing mode
                self.lastPoint = event.pos()    # save the location of the mouse press as the lastPoint
                # print the lastPoint for debigging purposes
            elif self.Paint == Paint.Line:
                """
                Else if the Paint is set to Line. 
                when a second click is done line is drawn.
                """
                if self.lastPoint == QPoint():
                    self.lastPoint = event.pos()
                else:
                    painter = QPainter(self.image)  # object which allows drawing to take place on an image
                    painter.setPen(QPen(self.brushColor, self.brushSize, self.brushStyle, self.brushCap, self.brushJoin))
                    painter.drawLine(self.lastPoint, event.pos())
                    self.lastPoint = QPoint()

            # Tells the library to update the widget, as something might have been drawn.
            self.update()

        """
        Method is called when the mouse is moved.
        It's only used in this case if the Paint is set to StartPoint and the user continues to draw while moving the mouse.
        """
    def mouseMoveEvent(self, event):                        # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-5/qwidget.html#mouseMoveEvent
        if event.buttons() & Qt.LeftButton & self.drawing & (self.Paint == Paint.StartPoint):     # if there was a press, and it was the left button and we are in drawing mode
            painter = QPainter(self.image)                  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-5/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, self.brushStyle, self.brushCap, self.brushJoin))
            painter.drawLine(self.lastPoint, event.pos())    # draw a line from the StartPoint of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()                     # set the last point to refer to the StartPoint we have just moved to, this helps when drawing the next line segment
            self.update()                                   # call the update method of the widget which calls the paintEvent of this class.

    def mouseReleaseEvent(self, event):                     # when the mouse is released, documentation: https://doc.qt.io/qt-5/qwidget.html#mouseReleaseEvent.
        if event.button == Qt.LeftButton:                   # if the released button is the left button, documenation: https://doc.qt.io/qt-5/qt.html#MouseButton-enum.
            # Saves the image before making any changes.
            self.savedImage = self.resizeSavedImage
            self.resizeSavedImage = self.image
            self.drawing = False                            # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(self)                      # create a new QPainter object, documenation: https://doc.qt.io/qt-5/qpainter.html
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect()) # draw the image , documentation: https://doc.qt.io/qt-5/qpainter.html#drawImage-1


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintingApplication()
    window.show()
    app.exec() # start the event loop running