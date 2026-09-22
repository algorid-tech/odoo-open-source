#################################################################
#                                                               #
#       Developed by Algorid                                    #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

{
    'name': 'Binary Drop Widget',
    'author': 'Algorid Limited',
    'website': 'https://www.algorid.com',
    'company': 'Algorid Limited',
    'maintainer': 'Algorid Limited',
    'category': 'Tools',
    'version': '20.0.1.0',
    'summary': 'Extends the binary widget so a file can be dropped on the field',
    'description': """
        Provides a new field widget called 'binary_drop' that works exactly like
        the standard binary widget but turns the field into a drop area: a file
        dragged from the desktop and dropped on it is uploaded straight away.
        The usual Upload / Download / Edit / Clear buttons are kept, and the
        accepted_file_extensions option is honoured for dropped files too.
    """,
    'license': 'LGPL-3',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'algorid_binary_drop/static/src/scss/binary_drop_field.scss',
            'algorid_binary_drop/static/src/xml/binary_drop_field.xml',
            'algorid_binary_drop/static/src/js/binary_drop_field.js',
        ],
    },
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
