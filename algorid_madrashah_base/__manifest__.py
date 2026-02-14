# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################
{
    'name': 'Madrashah Management - Base',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Base Module for Madrashah Management System',
    'description': """
        Madrashah Management System - Base Module
        ==========================================
        Foundation module for Madrashah (Islamic Educational Institution) Management.
        Features:
        ---------
        * Academic Year Management
        * Class Management
        * Section Management
        * Subject Management
        * Security Groups and Access Rights
        * Base Configuration
        Bilingual Support:
        ------------------
        * English and Bangla language support
    """,
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/madrashah_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/academic_year_views.xml',
        'views/class_views.xml',
        'views/section_views.xml',
        'views/subject_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu_views.xml',
    ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
