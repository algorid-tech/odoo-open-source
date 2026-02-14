# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Madrashah Management - Exams & Results',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Exam and Results Management for Madrashah',
    'description': """
        Madrashah Management System - Exams & Results Module
        =====================================================
        
        Comprehensive exam and results management for Islamic Educational Institutions.
        
        Features:
        ---------
        * Exam Calendar Creation
        * Exam Schedule Management
        * Marks Entry per Subject
        * Automatic Grade Calculation
        * GPA Calculation
        * Report Card Generation
        * Result Analysis
        
        Bilingual Support:
        ------------------
        * English and Bangla (বাংলা) language support
    """,
    'depends': ['algorid_madrashah_student', 'algorid_madrashah_hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/grade_data.xml',
        'views/exam_views.xml',
        'views/exam_result_views.xml',
        'views/grade_config_views.xml',
        'wizard/marks_entry_wizard_views.xml',
        'report/report_card.xml',
        'views/menu_views.xml',
    ],
    'images': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

