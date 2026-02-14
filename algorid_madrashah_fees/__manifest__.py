# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Madrashah Management - Fees',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Fees Management for Madrashah',
    'description': """
        Madrashah Management System - Fees Module
        ==========================================
        
        Comprehensive fees management for Islamic Educational Institutions.
        
        Features:
        ---------
        * Fee Structure Configuration (Monthly/Term)
        * Fee Types Management
        * Invoice Generation
        * Payment Tracking
        * Late Fee Calculation
        * Discount Management
        * Fee Reports
        * Integration with Odoo Accounting
        
        Bilingual Support:
        ------------------
        * English and Bangla (বাংলা) language support
    """,
    'depends': ['algorid_madrashah_student', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/fee_type_data.xml',
        'views/fee_structure_views.xml',
        'views/fee_type_views.xml',
        'views/student_fee_views.xml',
        'views/fee_discount_views.xml',
        'wizard/fee_invoice_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

