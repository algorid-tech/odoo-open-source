# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Madrashah Management - HR & Teachers',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Staff and Teacher Management for Madrashah',
    'description': """
        Madrashah Management System - HR & Teachers Module
        ===================================================
        
        Comprehensive staff and teacher management for Islamic Educational Institutions.
        
        Features:
        ---------
        * Teacher Profile Management
        * Subject and Class Assignment
        * Teacher Attendance Tracking
        * Work Schedule Management
        * Qualification Records
        * Experience History
        
        Bilingual Support:
        ------------------
        * English and Bangla (বাংলা) language support
    """,
    'depends': ['algorid_madrashah_base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/teacher_schedule_views.xml',
        'views/hr_employee_views.xml',
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

