'''
Created on 12/10/2014

@author: ferrari
'''
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *

class MultiLayerSelection(QgsMapTool):

    def __init__(self, canvas, action):
        self.canvas = canvas
        self.active = False
        QgsMapTool.__init__(self, self.canvas)
        self.setAction(action)
    
    def canvasPressEvent(self, e):
        p = self.toMapCoordinates(e.pos())
        layers = self.canvas.layers()
        w = self.canvas.mapUnitsPerPixel() * 3
        rect = QgsRectangle(p.x()-w, p.y()-w, p.x()+w, p.y()+w)
        for layer in layers:
            if layer.type() == QgsMapLayer.RasterLayer:
                continue
            lRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)
            layer.select(lRect, False)
    
    def deactivate(self):
        if self is not None:
            QgsMapTool.deactivate(self)
        
    def activate(self):
        QgsMapTool.activate(self)
    