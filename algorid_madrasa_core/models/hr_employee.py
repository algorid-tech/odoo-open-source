# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2025 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    """Inherits from hr.employee to add employee management features for Madrasa."""
    _inherit = 'hr.employee'

    employee_code = fields.Char(
        string='Employee Code',
        required=True,
        help='Unique code for the employee, used for identification purposes.'
    )


