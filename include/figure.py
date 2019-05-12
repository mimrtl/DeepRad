# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use("Qt5Agg")  # Use QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)    # Necessary
        self.axes = self.fig.add_subplot(111)
        #self.axes.hold(False)  # deprecated

