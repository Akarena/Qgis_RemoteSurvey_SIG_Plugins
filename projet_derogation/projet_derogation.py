# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjetDerogation
                                 A QGIS plugin
 Ce plugin est un outil pour la validité des dérogations.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-06-24
        git sha              : $Format:%H$
        copyright            : (C) 2021 by BOUSSIAR ILYAS
        email                : boussiar.ilyas@gmail.com
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
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

from qgis.core import *
from pathlib import Path


# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .projet_derogation_dialog import ProjetDerogationDialog
import processing
import os.path
import csv
import os, re


class ProjetDerogation:
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
            'ProjetDerogation_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Projet Dérogation')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ProjetDerogation', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/projet_derogation/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Projet Dérogation'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ProjetDerogationDialog()

        # show the dialog
        self.dlg.show()
        # LOGIC OF THE APP
        self.project = QgsProject.instance()
        self.layer_inter =  QgsVectorLayer('Polygon?crs=EPSG:1166&field=OBJECTID:string(25)&field=LAYER:string(25)&field=REFERENCE:string(25)&field=COMMUNE:string(25)&field=SUPERFICIE&field=POURCENTAGE', "zone_intersection" , "memory")
        self.removeAllAdditionalLayers()
        self.projectName = "project"
        self.dlg.pushButtonPos.clicked.connect(self.createPoint)
        self.dlg.pushButton.clicked.connect(self.buffer)
        self.dlg.pushButtonInt.clicked.connect(self.intersection)
        self.dlg.pushButtonPdf.clicked.connect(self.printpdf)
        self.dlg.pushButtonImage.clicked.connect(self.printimage)
        self.dlg.tableWidget.itemSelectionChanged.connect(self.itemSelection)  
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def removeAllAdditionalLayers(self):
        layers=["COLLECTIF","Derogation_central_13_avril","DOMAINE_FORESTIER","DOMAINE_PUBLIC","DOMIANE_PRIVE_ETAT","DOMAINE_COMMUNAL"]
        for layer in self.project.mapLayers().values():
            if layer.name() not in layers:
                self.project.removeMapLayer(layer.id())

    def findLayerByName(self, layerName):
            layer = list(filter(lambda layer: (layer.name() == layerName), self.layers))
            return layer[0] if layer else None
    
    def itemSelection(self):
        for currentQTableWidgetItem in self.dlg.tableWidget.selectedItems():
            self.removeAllSelection()
            table_row = currentQTableWidgetItem.row()
            layerName = self.dlg.tableWidget.item(table_row,1).text()
            column_dictionary={"0": "OBJECTID"}
            table_column=currentQTableWidgetItem.column()
            if str(table_column) in column_dictionary:
                req = column_dictionary[str(table_column)]+"=" + str(currentQTableWidgetItem.text())+" AND "+ "LAYER"+"="+str(layerName)
                print(req)
                self.selectByObjectIdAndLayerName(str(currentQTableWidgetItem.text()),layerName)
    def selectByObjectIdAndLayerName(self,objectId,layerName):
        for feature in self.layer_inter.getFeatures():
            if (feature.attribute('OBJECTID') == objectId) and (feature.attribute('LAYER')==layerName):
                self.layer_inter.select(feature.id())
                break


    def removeAllSelection(self):
        layers = ["zone_intersection","COLLECTIF","Derogation_central_13_avril","DOMAINE_FORESTIER","DOMAINE_PUBLIC","DOMIANE_PRIVE_ETAT","DOMAINE_COMMUNAL"]
        for layerName in layers:
            layer = self.project.mapLayersByName(layerName)[0]
            layer.removeSelection()

    def intersection(self):
        buffer_inter = self.project.mapLayersByName("zone_projet")
        if len(buffer_inter) > 0 :
            buffer_inter = buffer_inter[0]
            self.iface.setActiveLayer(buffer_inter)
            self.iface.zoomToActiveLayer()
            self.dlg.tableWidget.setRowCount(0)
            if int(self.layer_inter.featureCount())!=0:
                feats=self.layer_inter.getFeatures()
                self.layer_inter.startEditing()
                for fid in feats:
                    self.layer_inter.deleteFeature(fid.id())
                self.layer_inter.commitChanges()
                self.layer_inter.updateExtents()
            field_names = ['OBJECTID','Layer', 'Reference', 'Commune', 'Superficie (m2)', 'Pourcentage']
            self.dlg.tableWidget.setHorizontalHeaderLabels(field_names)
            row_number = 0
            pr = self.layer_inter.dataProvider()
            self.layer_inter.startEditing()
            for layer in self.project.mapLayers().values():
                print(layer.name())
                if(layer.name() not in {"zone_projet",self.projectName,"zone_intersection"}):
                    for featureLayer in layer.getFeatures():
                        for bufferFeature in buffer_inter.getFeatures():
                            if featureLayer.geometry().intersects(bufferFeature.geometry()):
                                geom = featureLayer.geometry().intersection(bufferFeature.geometry())
                                intersection_area = geom.area()
                                fet = QgsFeature()
                                fet.setGeometry(geom)
                                pourcentage=str(round((intersection_area/featureLayer.geometry().area())*100, 2)) + '%'
                                attributesFeature = featureLayer.attributes()
                                print("layer")
                                print(attributesFeature)
                                fet.setAttributes([attributesFeature[0],layer.name(),attributesFeature[3 if layer.name()!="Derogation_central_13_avril" else 6],attributesFeature[7 if layer.name()!="Derogation_central_13_avril" else 3],attributesFeature[10 if layer.name()!="Derogation_central_13_avril" else 8],pourcentage])
                                pr.addFeatures([fet])
                                self.afficher_inter(featureLayer, row_number, pourcentage,layer.name())
                                row_number += 1
            self.layer_inter.commitChanges()
            self.layer_inter.updateExtents()
            self.project.addMapLayers([self.layer_inter])
        else:
            QMessageBox.information(None, "Message d'erreur", "le buffer est manquant, essay de le créer avant clicker sur intersection")


    def afficher_inter(self, row_data, row_number, pourcentage,layerName):
        self.dlg.tableWidget.insertRow(row_number)
        column = 0
        if layerName!="Derogation_central_13_avril":
            for column_number, data in enumerate(row_data.attributes()):
                if column_number in [0,1,3,7,10] :
                    self.dlg.tableWidget.setItem(row_number, column, QTableWidgetItem(str(layerName if (column_number==1) else  data)))
                    column += 1
        else :
            self.dlg.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(row_data.attribute('OBJECTID'))))
            self.dlg.tableWidget.setItem(row_number, 1, QTableWidgetItem(layerName))
            self.dlg.tableWidget.setItem(row_number, 2, QTableWidgetItem(str(row_data.attribute('Ref_foncie'))))
            self.dlg.tableWidget.setItem(row_number, 3, QTableWidgetItem(str(row_data.attribute('Commune'))))
            self.dlg.tableWidget.setItem(row_number, 4, QTableWidgetItem(str(row_data.attribute('Superficie'))))
        self.dlg.tableWidget.setItem(row_number, 5 , QTableWidgetItem(pourcentage))

    def buffer(self):
            canvas = self.iface.mapCanvas()
            point = self.project.mapLayersByName(self.projectName)
            if len(point) > 0:
                point = point[0]
                layer_buff = self.project.mapLayersByName('zone_projet')
                if len(layer_buff) == 0 :
                    layer_buff =  QgsVectorLayer('Polygon?crs=EPSG:1166&field=ID:string(25)&field=SURFACE:string(25)', 'zone_projet' , "memory")
                else:
                    layer_buff=layer_buff[0]
                bfr=self.dlg.spinBox.value()

                bfr=float(bfr)
                if bfr > 1000 :
                    QMessageBox.information(None, "Message d'erreur", "buffer il faut etre moins de 1000")
                    #suprimer tous les donnee precedement enregistres
                else :
                    if int(layer_buff.featureCount())!=0:
                        feats=layer_buff.getFeatures()
                        layer_buff.startEditing()
                        for fid in feats:
                            layer_buff.deleteFeature(fid.id())
                        layer_buff.commitChanges()
                        layer_buff.updateExtents()
                    
                    pr = layer_buff.dataProvider()
                    layer_buff.startEditing()
                    # creation de nouveau Buffer avec integration de l'identifiant 
                    for elem in point.getFeatures():
                        geom = elem.geometry()
                        buffer = geom.buffer(bfr,20)
                        seg = QgsFeature()
                        seg.setGeometry(buffer)
                        seg.setAttributes([1,buffer.area()])
                        pr.addFeatures([seg])
                    layer_buff.commitChanges()
                    layer_buff.updateExtents()
                   #   Ajout de la couche
                    symbol = layer_buff.renderer().symbol()
                    symbol.setColor(QColor('#fb9a99'))
                    symbol.setOpacity(0.65)
                    self.project.addMapLayers([layer_buff])
                    self.iface.setActiveLayer(layer_buff)
                    self.iface.zoomToActiveLayer()
            else:
                QMessageBox.information(None, "Message d'erreur", "le point est manquant, essay de le créer avant clicker sur buffer")

    def configurePrintOut(self):
        manager=self.project.layoutManager()
        layoutName="Result"
        layout_list=manager.printLayouts()
        for layout in layout_list:
            if layout.name() == layoutName:
                manager.removeLayout(layout)

        #add a new layout
        zone_buffer = self.project.mapLayersByName('zone_projet')[0]
        layout=QgsPrintLayout(self.project)
        layout.initializeDefaults()
        layout.setName(layoutName)
        manager.addLayout(layout)

        #create a map item in the layout
        map=QgsLayoutItemMap(layout)
        map.setRect(20,20,20,20)

        #set the map extent
        ms=QgsMapSettings()
        ms.setLayers([zone_buffer])
        rect=QgsRectangle(ms.fullExtent())
        rect.scale(1)

        ms.setExtent(rect)
        map.setExtent(rect)
        map.setBackgroundColor(QColor(255,255,255,0))
        layout.addLayoutItem(map)

        map.attemptMove(QgsLayoutPoint(113.018,15,QgsUnitTypes.LayoutMillimeters))
        map.attemptResize(QgsLayoutSize(183.982,195,QgsUnitTypes.LayoutMillimeters))

        legend = QgsLayoutItemLegend(layout)
        legend.setTitle("Legend")
        layout.addLayoutItem(legend)
        legend.attemptMove(QgsLayoutPoint(0,15,QgsUnitTypes.LayoutMillimeters))

        scalebar=QgsLayoutItemScaleBar(layout)
        scalebar.setStyle('Single Box')
        scalebar.setLinkedMap(map)
        scalebar.applyDefaultSize(QgsUnitTypes.DistanceKilometers)
        layout.addLayoutItem(scalebar)
        scalebar.attemptMove(QgsLayoutPoint(125.003,190.542,QgsUnitTypes.LayoutMillimeters))

        title=QgsLayoutItemLabel(layout)
        title.setText("Carte de Dérogation du projet "+("" if self.projectName=="project"else self.projectName))
        font = QFont('Arial',20)
        font.setBold(True)
        title.setFont(font)
        layout.addLayoutItem(title)
        title.adjustSizeToText()
        title.attemptMove(QgsLayoutPoint(85.053,3.769,QgsUnitTypes.LayoutMillimeters))
        
        conditions = self.checkCondition()

        decision=QgsLayoutItemLabel(layout)
        decision.setText("Décision finale:"+("Favorable" if (len(conditions) ==0) else "Défavorable" ))
        font = QFont('Arial',20)
        font.setBold(True)
        decision.setFont(font)
        decision.setFontColor(QColor('#19f000' if (len(conditions) ==0) else '#f40409' ))
        layout.addLayoutItem(decision)
        decision.adjustSizeToText()
        decision.attemptMove(QgsLayoutPoint(8.403,176.613,QgsUnitTypes.LayoutMillimeters))

        decisionReason=QgsLayoutItemLabel(layout)
        decisionReason.setText("" if (len(conditions) ==0) else ("Raison: la zone contient:\n-("+','.join(conditions)+")"))
        font = QFont('Arial',20)
        decisionReason.setFont(font)
        layout.addLayoutItem(decisionReason)
        decisionReason.adjustSizeToText()
        decisionReason.attemptMove(QgsLayoutPoint(8.403,186.492,QgsUnitTypes.LayoutMillimeters))
        decisionReason.attemptResize(QgsLayoutSize(86.740,20,QgsUnitTypes.LayoutMillimeters)) 
        #10 20

        northArrow = QgsLayoutItemPicture(layout)
        northArrow.setPicturePath("C:\\Program Files\\QGIS 3.16\\apps\\qgis-ltr\\svg\\arrows\\Arrow_05.svg")
        northArrow.setMode(QgsLayoutItemPicture.FormatSVG)
        northArrow.setNorthMode(QgsLayoutItemPicture.TrueNorth)
        layout.addLayoutItem(northArrow)
        northArrow.attemptMove(QgsLayoutPoint(119.024,19.023,QgsUnitTypes.LayoutMillimeters))
        northArrow.attemptResize(QgsLayoutSize(11.958,11.958,QgsUnitTypes.LayoutMillimeters))
        rowNumberReal=0
        for row in range(self.dlg.tableWidget.rowCount()):
            if self.dlg.tableWidget.item(row,0).text():
                rowNumberReal+=1

        layout_html = QgsLayoutItemHtml(layout)
        html_frame = QgsLayoutFrame(layout, layout_html)
        html_frame.attemptSetSceneRect(QRectF(0.150, 90, 112.718, (8 + (11*rowNumberReal))))
        html_frame.setFrameEnabled(True)
        layout_html.addFrame(html_frame)
        layout_html.setContentMode(QgsLayoutItemHtml.ManualHtml)
        html ='<table ><tr><th>OBJECTID</th><th>Reference</th><th>Commune</th><th>Superficie</th><th>Pourcentage</th></tr>'
        
        for row in range(self.dlg.tableWidget.rowCount()):
            data=[]
            for column in range(self.dlg.tableWidget.columnCount()):
                if not self.dlg.tableWidget.item(row,0).text():
                    break
                if column ==1:
                    continue
                data.append(self.dlg.tableWidget.item(row,column).text())
            if len(data)>0:
                html = html + '<tr><td>'+data[0]+'</td><td>'+data[1]+'</td><td>'+data[2]+'</td><td>'+data[3]+'</td><td>'+data[4]+'</td></tr>'


        html = html+'</table>'
        layout_html.setHtml(html)
        layout_html.loadHtml()

        exporter=QgsLayoutExporter(layout)
        return exporter    
    
    def checkCondition(self):
            conditions=[]
            foretCondition=0
            publicCondition = 0
            derogationCondition = 0
            for row in range(self.dlg.tableWidget.rowCount()):
                layer = self.dlg.tableWidget.item(row,1).text()
                if layer== "DOMAINE_FORESTIER":
                    foretCondition=1
                if layer== "DOMAINE_PUBLIC":
                    publicCondition = 1
                if layer== "Derogation_central_13_avril":
                    derogationCondition += 1
            if foretCondition==1:
                conditions.append("FORET")
            if publicCondition==1:
                conditions.append("PUBLIC")
            if derogationCondition >5 :
                conditions.append(str(derogationCondition)+"Dérogation")
            return conditions
    def printpdf(self):
        if len(list(self.layer_inter.getFeatures())) >0:
            exporter = self.configurePrintOut()
            exporter.exportToPdf(self.project.readPath("./")+'\\result_'+self.projectName+'.pdf',QgsLayoutExporter.PdfExportSettings())
        else:
            QMessageBox.information(None, "Message d'erreur", "aucun intersection")


    def printimage(self):
        if  len(list(self.layer_inter.getFeatures())) >0:
            exporter = self.configurePrintOut()
            exporter.exportToImage(self.project.readPath("./")+'\\result_'+self.projectName+'.jpg',QgsLayoutExporter.ImageExportSettings())
        else:
            QMessageBox.information(None, "Message d'erreur", "aucun intersection")
    
    def updatePoint(self,pointLayer):
        if (pointLayer.name() == self.dlg.lineEditProjectName.text()):
            feats=pointLayer.getFeatures()
            pr = pointLayer.dataProvider()
            pointLayer.startEditing()
            for fid in feats:
                pointLayer.deleteFeature(fid.id())
            point = QgsPointXY(float(self.dlg.spinBoxX.value()), float(self.dlg.spinBoxY.value()))
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(point))
            feat.setAttributes([1,self.dlg.spinBoxX.text(),self.dlg.spinBoxY.text()])
            pr.addFeatures([feat])
            pointLayer.commitChanges()
            pointLayer.updateExtents()
        else :
            self.project.removeMapLayer(pointLayer.id())
            self.createPoint()

    def createPoint(self):
        lay = self.project.mapLayersByName(self.projectName)
        if len(lay)>0:
            lay = lay[0]
            self.updatePoint(lay)
        else:
            self.projectName = self.dlg.lineEditProjectName.text() if self.dlg.lineEditProjectName.text() else "project"
            pointLayer =  QgsVectorLayer('Point?crs=EPSG:1166&field=OBJECTID:string(25)&field=X:string(25)&field=Y:string(25)', self.projectName , "memory")
            pr = pointLayer.dataProvider()
            pointLayer.startEditing()
            # for fid in feats:
            point = QgsPointXY(float(self.dlg.spinBoxX.value()), float(self.dlg.spinBoxY.value()))
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(point))
            feat.setAttributes([1,self.dlg.spinBoxX.text(),self.dlg.spinBoxY.text()])
            pr.addFeatures([feat])
            pointLayer.commitChanges()
            pointLayer.updateExtents()
            self.project.addMapLayers([pointLayer])
