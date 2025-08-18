# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2025 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Madrasa Core',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'category': 'Education',
    'version': '18.0',
    'price': 0.0,
    'currency': 'USD',
    'summary': """Core module for Madrasa Management""",
    'description': """
This module provides the core features of Madrasa management:
- Student & guardian management
- Teacher/ustadh management
- Classes & subjects (Islamic & general)
- Hifz progress tracking
===========================
Developed by Algorid Limited   
    """,
    'license': 'OPL-1',
    'depends': ['base', 'contacts', 'hr'],
    'data': [
        'data/sequence.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [],
    # 'images': [
    #     'static/description/banner.jpg'
    # ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
