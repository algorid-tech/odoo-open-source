# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Madrashah Management - Timetable',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Timetable Management for Madrashah',
    'description': """
        Madrashah Management System - Timetable Module
        ===============================================
        
        Comprehensive timetable management for Islamic Educational Institutions.
        
        Features:
        ---------
        * Weekly Timetable Builder
        * Period/Slot Configuration
        * Class-wise Timetable
        * Teacher-wise Timetable
        * Conflict Detection
        * Timetable Export (PDF/CSV)
        
        Bilingual Support:
        ------------------
        * English and Bangla (বাংলা) language support
    """,
    'depends': ['algorid_madrashah_hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/period_data.xml',
        'views/timetable_views.xml',
        'views/period_views.xml',
        'views/menu_views.xml',
        'report/timetable_report.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

