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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *
from MultiLayerSelection import MultiLayerSelection
# Initialize Qt resources from file resources.py
import resources

import os.path



class MultLayerSelection:
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

 
 
    def initGui(self):
        # Create action that will start plugin configuration
        self.actionCriar = QAction(
            QIcon(":/plugins/MultipleLayerSelection/icon.png"),
            u"Multiple Layer Selection", self.iface.mainWindow())
        # connect the action to the run method
        self.actionCriar.setCheckable(True)
        self.actionCriar.toggled.connect(self.run)
        
        self.tool = MultiLayerSelection(self.iface.mapCanvas(), self.actionCriar) 
        #self.iface.mapCanvas().setMapTool(tool)
        
        

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionCriar)
     

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removeToolBarIcon(self.actionCriar)

    def run(self, b):
        if b:
            self.iface.mapCanvas().setMapTool(self.tool)
            self.iface.mapCanvas().mapToolSet.connect(self.desconecta)
        else:
            self.tool.deactivate()
            
    def desconecta(self, mapTool):
        self.tool.deactivate()
