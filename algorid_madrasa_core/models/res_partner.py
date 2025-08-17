# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2025 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields


class ResPartner(models.Model):
    """Inherits from res.partner to add student and guardian management features."""
    _inherit = 'res.partner'

    student_code = fields.Char(
        string='Student Code',
        required=True,
        help='Unique code for the student, used for identification purposes.'
    )


