# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SentinelDownloader
                                 A QGIS plugin
 This plugin is done to download Sentinel 1 data based on a few criterias
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-06-23
        copyright            : (C) 2021 by Malak IRJA - Ilyasse Boussiar
        email                : irjamalak@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SentinelDownloader class from file SentinelDownloader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .sentinel_down import SentinelDownloader
    return SentinelDownloader(iface)
