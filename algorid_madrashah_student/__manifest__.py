# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Madrashah Management - Student',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Student Management for Madrashah',
    'description': """
        Madrashah Management System - Student Module
        =============================================
        
        Comprehensive student management for Islamic Educational Institutions.
        
        Features:
        ---------
        * Student Profile Management
        * Guardian/Parent Information
        * Class and Section Assignment
        * Student Documents Management
        * Status Tracking (Active, Graduated, Left)
        * Student Tagging (Scholarship, Special Needs, etc.)
        * Student Photo Management
        * Enrollment History
        
        Bilingual Support:
        ------------------
        * English and Bangla (বাংলা) language support
    """,
    'depends': ['algorid_madrashah_base', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/tag_data.xml',
        'views/student_views.xml',
        'views/guardian_views.xml',
        'views/student_tag_views.xml',
        'views/student_document_views.xml',
        'views/menu_views.xml',
        'report/student_id_card_report.xml',
    ],
    'images': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

