# -*- coding: utf-8 -*-
def classFactory(iface):
    from .show_all_layers_crs import ShowAllLayersCRS
    return ShowAllLayersCRS(iface)