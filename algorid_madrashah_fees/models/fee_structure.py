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


class FeeStructure(models.Model):
    _name = 'algorid.fee.structure'
    _description = 'Fee Structure'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'academic_year_id desc, class_id'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
    )
    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
        required=True,
        tracking=True,
    )
    class_id = fields.Many2one(
        'algorid.class',
        string='Class',
        required=True,
        tracking=True,
    )
    line_ids = fields.One2many(
        'algorid.fee.structure.line',
        'structure_id',
        string='Fee Lines',
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total',
        store=True,
    )
    monthly_amount = fields.Float(
        string='Monthly Amount',
        compute='_compute_total',
        store=True,
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
    notes = fields.Text(
        string='Notes',
    )

    _sql_constraints = [
        ('unique_structure', 'unique(academic_year_id, class_id, company_id)',
         'Fee structure for this class and academic year already exists!'),
    ]

    @api.depends('academic_year_id', 'class_id')
    def _compute_name(self):
        for record in self:
            if record.academic_year_id and record.class_id:
                record.name = f"{record.class_id.name} - {record.academic_year_id.name}"
            else:
                record.name = "New Fee Structure"

    @api.depends('line_ids', 'line_ids.amount')
    def _compute_total(self):
        for record in self:
            total = sum(record.line_ids.mapped('amount'))
            monthly = sum(record.line_ids.filtered(
                lambda l: l.fee_type_id.frequency == 'monthly'
            ).mapped('amount'))
            record.total_amount = total
            record.monthly_amount = monthly


class FeeStructureLine(models.Model):
    _name = 'algorid.fee.structure.line'
    _description = 'Fee Structure Line'
    _order = 'sequence, fee_type_id'

    structure_id = fields.Many2one(
        'algorid.fee.structure',
        string='Fee Structure',
        required=True,
        ondelete='cascade',
    )
    fee_type_id = fields.Many2one(
        'algorid.fee.type',
        string='Fee Type',
        required=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    amount = fields.Float(
        string='Amount',
        required=True,
    )
    due_day = fields.Integer(
        string='Due Day',
        default=10,
        help='Day of month when this fee is due',
    )
    is_mandatory = fields.Boolean(
        string='Mandatory',
        default=True,
    )
    notes = fields.Char(
        string='Notes',
    )

    @api.onchange('fee_type_id')
    def _onchange_fee_type_id(self):
        if self.fee_type_id:
            self.amount = self.fee_type_id.default_amount

