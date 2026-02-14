# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Madrashah Management - Portal',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Portal Access for Parents and Students',
    'description': """
        Madrashah Management System - Portal Module
        ============================================
        
        Portal access for parents and students.
        
        Features:
        ---------
        * View Student Profile
        * View Attendance Records
        * View Fee Status and Payment History
        * View Exam Results and Report Cards
        * View Class Timetable
        
        Bilingual Support:
        ------------------
        * English and Bangla (বাংলা) language support
    """,
    'depends': [
        'portal',
        'algorid_madrashah_student',
        'algorid_madrashah_attendance',
        'algorid_madrashah_fees',
        'algorid_madrashah_exam',
        'algorid_madrashah_timetable',
    ],
    'data': [
        'security/portal_security.xml',
        'views/portal_templates.xml',
    ],
    'images': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

