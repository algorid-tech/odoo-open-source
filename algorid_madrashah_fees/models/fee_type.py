# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _


class FeeType(models.Model):
    _name = 'algorid.fee.type'
    _description = 'Fee Type'
    _order = 'sequence, name'

    name = fields.Char(
        string='Fee Type',
        required=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Fee Type (Bangla)',
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    fee_category = fields.Selection([
        ('tuition', 'Tuition Fee'),
        ('admission', 'Admission Fee'),
        ('exam', 'Exam Fee'),
        ('transport', 'Transport Fee'),
        ('hostel', 'Hostel Fee'),
        ('library', 'Library Fee'),
        ('lab', 'Lab Fee'),
        ('sports', 'Sports Fee'),
        ('other', 'Other'),
    ], string='Category', default='tuition', required=True)
    is_recurring = fields.Boolean(
        string='Recurring',
        default=True,
        help='If checked, this fee will be charged periodically',
    )
    frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half Yearly'),
        ('yearly', 'Yearly'),
        ('one_time', 'One Time'),
    ], string='Frequency', default='monthly')
    default_amount = fields.Float(
        string='Default Amount',
        default=0.0,
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain="[('type', '=', 'service')]",
        help='Product used for invoicing',
    )
    account_id = fields.Many2one(
        'account.account',
        string='Income Account',
        domain="[('account_type', '=', 'income')]",
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    description = fields.Text(
        string='Description',
        translate=True,
    )

    _sql_constraints = [
        ('code_unique', 'unique(code, company_id)',
         'Fee type code must be unique!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('product_id'):
                # Create a product for this fee type
                product = self.env['product.product'].create({
                    'name': vals.get('name'),
                    'type': 'service',
                    'sale_ok': True,
                    'purchase_ok': False,
                    'list_price': vals.get('default_amount', 0),
                })
                vals['product_id'] = product.id
        return super().create(vals_list)

