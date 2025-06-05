from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog, QVBoxLayout, QTextEdit
import os

class ShowAllLayersCRS(QObject):

    def __init__(self, iface: QgisInterface):
        super().__init__()
        self.iface = iface
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        self.action = QAction(QIcon(icon_path), "Afficher SCR des couches", self.iface.mainWindow())
        self.action.triggered.connect(self.show_crs)

    def initGui(self):
        self.iface.addPluginToMenu("&Mon Plugin", self.action)
        self.iface.addToolBarIcon(self.action)

    def show_crs(self):
        layers = QgsProject.instance().mapLayers().values()
        layer_tree_root = QgsProject.instance().layerTreeRoot()
        
        # Préparation du contenu à afficher
        result_text = """
        <style>
            table { width: 100%; border-collapse: collapse; }
            th { background-color: #4C4C4C; color: white; padding: 8px; }
            td { padding: 8px; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            tr:nth-child(odd) { background-color: #d9d9d9; }
        </style>
        <table>
        <tr><th>Layer name</th><th>File type</th><th>Geometric type</th><th>Feature count</th><th>On Display</th><th>SCR</th><th>Updated Spatial Index</th></tr>
        """
        
        for layer in layers:
            layer_node = layer_tree_root.findLayer(layer.id())
            if layer_node:
                is_visible = layer_node.isVisible()
                source = layer.source()
                file_extension = os.path.splitext(source)[-1].lower()
                if file_extension == '.shp':
                    file_type = "SHP"
                elif file_extension == '.csv':
                    file_type = "CSV"
                else:
                    file_type = "Other"
                
                if isinstance(layer, QgsVectorLayer):
                    feature_count = layer.featureCount()
                    geom_type = QgsWkbTypes.displayString(layer.wkbType())
                    if "Point" in geom_type:
                        geom_type_str = "Point"
                    elif "LineString" in geom_type:
                        geom_type_str = "Line"
                    elif "Polygon" in geom_type:
                        geom_type_str = "Surface"
                    else:
                        geom_type_str = "Other"
                    
                    spatial_index = "X" if layer.hasSpatialIndex() else ""
                else:
                    feature_count = "N/A"
                    geom_type_str = "N/A"
                    spatial_index = "N/A"
                
                result_text += f"<tr><td>{layer.name()}</td><td>{file_type}</td><td>{geom_type_str}</td><td>{feature_count}</td><td>{'X' if is_visible else ''}</td><td>{layer.crs().authid()}</td><td>{spatial_index}</td></tr>"
        
        result_text += "</table>"
        
        # Création de la boîte de dialogue
        dialog = QDialog(self.iface.mainWindow())
        dialog.setWindowTitle("SCR des Couches")
        dialog.setMinimumSize(800, 600)
        
        # Utilisation d'un QTextEdit pour afficher le contenu
        text_edit = QTextEdit()
        text_edit.setHtml(result_text)
        text_edit.setReadOnly(True)  # Pour éviter la modification du texte
        
        # Ajout de QTextEdit dans un layout
        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        dialog.setLayout(layout)
        
        # Affichage de la boîte de dialogue
        dialog.exec_()

    def unload(self):
        self.iface.removePluginMenu("&Mon Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

def classFactory(iface: QgisInterface):
    return ShowAllLayersCRS(iface)