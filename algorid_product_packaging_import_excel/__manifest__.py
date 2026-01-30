# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2025 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Product Packaging Import from Excel',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Import product packaging from Excel files',
    'description': """
        Import Product Packaging from Excel
        ====================================
        
        Features:
        ---------
        * Import product packaging from Excel files (.xls, .xlsx)
        * Download Excel template with instructions
        * Create new or update existing packaging
        * Support for all packaging fields
        * Bulk import multiple packaging records
        * Error reporting and validation
        * Smart buttons on product template and product variant
        * Filter import by specific product or template
        
        Usage:
        ------
        Method 1: From Configuration Menu
        1. Go to Inventory > Configuration > Import Packaging
        2. Download the Excel template
        3. Fill in your packaging data
        4. Upload and import
        
        Method 2: From Product Form
        1. Open any product template or variant
        2. Click the "Import Packaging" button
        3. Download template (pre-filled with product info)
        4. Fill in packaging data
        5. Upload and import (automatically filtered to that product)
        
        Supported Fields:
        ----------------
        - Product Code/ID (required)
        - Packaging Name (required)
        - Contained Quantity (required)
        - Sequence
        - Barcode
        - Package Type
        - Sales (TRUE/FALSE)
        - Purchase (TRUE/FALSE)
        - Routes (comma-separated)
    """,
    'depends': ['product', 'stock'],
    'external_dependencies': {
        'python': ['openpyxl', 'xlrd'],
    },
    'data': [
        'security/ir.model.access.csv',
        'wizards/product_packaging_import_wizard_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
