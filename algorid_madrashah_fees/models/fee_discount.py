# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FeeDiscount(models.Model):
    _name = 'algorid.fee.discount'
    _description = 'Fee Discount'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Discount Name',
        required=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Discount Name (Bangla)',
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    discount_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], string='Discount Type', required=True, default='percentage')
    value = fields.Float(
        string='Value',
        required=True,
        help='Percentage (0-100) or Fixed Amount',
    )
    applies_to = fields.Selection([
        ('all', 'All Fees'),
        ('tuition', 'Tuition Only'),
        ('specific', 'Specific Fee Types'),
    ], string='Applies To', default='all', required=True)
    fee_type_ids = fields.Many2many(
        'algorid.fee.type',
        'discount_fee_type_rel',
        'discount_id',
        'fee_type_id',
        string='Fee Types',
    )
    eligibility = fields.Selection([
        ('all', 'All Students'),
        ('sibling', 'Sibling Discount'),
        ('scholarship', 'Scholarship'),
        ('staff_child', 'Staff Child'),
        ('orphan', 'Orphan'),
        ('merit', 'Merit Based'),
        ('need', 'Need Based'),
        ('other', 'Other'),
    ], string='Eligibility', default='all')
    max_discount = fields.Float(
        string='Maximum Discount Amount',
        help='Maximum discount amount (0 for no limit)',
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
         'Discount code must be unique!'),
    ]

    @api.constrains('discount_type', 'value')
    def _check_value(self):
        for record in self:
            if record.value < 0:
                raise ValidationError(_('Discount value cannot be negative!'))
            if record.discount_type == 'percentage' and record.value > 100:
                raise ValidationError(_('Percentage discount cannot exceed 100%!'))

    def calculate_discount(self, amount):
        """Calculate discount amount based on original amount."""
        self.ensure_one()
        if self.discount_type == 'percentage':
            discount = amount * (self.value / 100)
        else:
            discount = self.value

        if self.max_discount and discount > self.max_discount:
            discount = self.max_discount

        return min(discount, amount)

