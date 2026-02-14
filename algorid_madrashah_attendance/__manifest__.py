# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Madrashah Management - Attendance',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Attendance Management for Madrashah',
    'description': """
        Madrashah Management System - Attendance Module
        ================================================
        
        Comprehensive attendance management for Islamic Educational Institutions.
        
        Features:
        ---------
        * Student Daily Attendance
        * Teacher Attendance
        * Batch Attendance Entry
        * Attendance Reports and Dashboard
        * Export to CSV
        * Monthly Attendance Summary
        * Attendance Notifications
        
        Bilingual Support:
        ------------------
        * English and Bangla (বাংলা) language support
    """,
    'depends': ['algorid_madrashah_student', 'algorid_madrashah_hr'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/attendance_wizard_views.xml',
        'views/student_attendance_views.xml',
        'views/teacher_attendance_views.xml',
        'views/menu_views.xml',
        'report/attendance_report.xml',
    ],
    'images': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

