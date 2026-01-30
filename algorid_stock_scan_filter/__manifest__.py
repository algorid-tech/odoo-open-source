# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2025 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Stock Picking Scan Filter',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Add scan status filters to Barcode Inventory Operations',
    'description': """
        Stock Picking Scan Status Filter
        =================================
        
        This module adds scan status filters to stock pickings:
        
        * **Not Scanned**: 0 items scanned (quantity = 0)
        * **Partially Scanned**: Some items scanned but not all (0 < quantity < demand)
        * **Fully Scanned**: All items scanned (quantity >= demand)
        
        Features:
        ---------
        * Filter pickings by scan status
        * Group by scan status
        * Computed field that updates automatically
    """,
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
