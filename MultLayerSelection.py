# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Multi Layer Selection
                                 A QGIS plugin
                              -------------------
        begin                : 2014-10-07
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Felipe Ferrari
        email                : ferrari@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import absolute_import
from builtins import object
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtWidgets import QToolButton, QAction
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsMapLayer
from .MultiLayerSelection import MultiLayerSelection
from .MultiLayerRectangleSelection import MultiLayerRectangleSelection
# Initialize Qt resources from file resources.py
from . import resources

import os.path

class MultLayerSelection(object):
    """QGIS Plugin Implementation."""
    
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MultLayerSelection_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
                
        self.toolbar = self.iface.addToolBar(u'MultipleSelection')
        self.toolbar.setObjectName(u'MultipleSelection')
        self.actionList = []

    def createToolButton(self, parent, text):
        button = QToolButton(parent)
        button.setObjectName(text)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button.setPopupMode(QToolButton.MenuButtonPopup)
        parent.addWidget(button)
        return button
    
    def createAction(self, icon_path, text, callback, checkable=True):
        action = QAction(
            QIcon(icon_path),
            text,
            self.iface.mainWindow())
        # connect the action to the run method
        action.setCheckable(checkable)
        if checkable:
            action.toggled.connect(callback)
        else:
            action.triggered.connect(callback)
        self.iface.registerMainWindowAction(action, '')
        self.actionList.append(action)
        return action
 
    def initGui(self):
        # Create action that will start plugin configuration
        self.actionCriar = self.createAction(":/plugins/MultipleLayerSelection/icon.png",
                                            u"Multi Selection by point",
                                            self.run)

        # Create action that will start plugin configuration
        self.actionCriarRectangle = self.createAction(":/plugins/MultipleLayerSelection/icon_rectangle.png",
                                                      u"Multiple Selection by Rectangle",
                                                      self.runRectangle)

        # Create action that will start plugin configuration
        self.actionClear = self.createAction(":/plugins/MultipleLayerSelection/icon_clear.png",
                                                      u"Clear selections",
                                                      self.clear,
                                                      checkable=False)
                
        self.tool = MultiLayerSelection(self.iface.mapCanvas(), self.actionCriar) 
        self.toolRectangle = MultiLayerRectangleSelection(self.iface.mapCanvas(), self.actionCriarRectangle) 
        
        #QToolButtons
        self.selectionButton = self.createToolButton(self.toolbar, u'MultipleSelectionButton')
        self.selectionButton.addAction(self.actionCriar)     
        self.selectionButton.addAction(self.actionCriarRectangle)
        self.selectionButton.addAction(self.actionClear)
        self.selectionButton.setDefaultAction(self.actionCriar)    

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.mainWindow().removeToolBar(self.toolbar)
        for action in self.actionList:
            try:
                self.iface.unregisterMainWindowAction(action)
            except:
                pass
        self.tool.deactivate()
        self.toolRectangle.deactivate()
        
    def clear(self):
        try:
            self.selectionButton.setDefaultAction(self.actionClear)
        except:
            pass
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.type() == QgsMapLayer.RasterLayer:
                continue
            layer.removeSelection()

    def run(self, b):
        if b:
            try:
                self.selectionButton.setDefaultAction(self.actionCriar)
            except:
                pass
            self.iface.mapCanvas().setMapTool(self.tool)
        else:
            self.iface.mapCanvas().unsetMapTool(self.tool)

    def runRectangle(self, b):
        if b:
            try:
                self.selectionButton.setDefaultAction(self.actionCriarRectangle)
            except:
                pass
            self.iface.mapCanvas().setMapTool(self.toolRectangle)
        else:
            self.iface.mapCanvas().unsetMapTool(self.toolRectangle)
            
