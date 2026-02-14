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
class AcademicYear(models.Model):
    _name = 'algorid.academic.year'
    _description = 'Academic Year'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'
    name = fields.Char(
        string='Academic Year',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
        tracking=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
        tracking=True,
    )
    is_current = fields.Boolean(
        string='Current Academic Year',
        default=False,
        tracking=True,
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
    )
    _sql_constraints = [
        ('code_unique', 'unique(code, company_id)', 
         'Academic year code must be unique!'),
        ('name_unique', 'unique(name, company_id)', 
         'Academic year name must be unique!'),
    ]
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date >= record.end_date:
                    raise ValidationError(_('End Date must be after Start Date!'))
    @api.constrains('is_current')
    def _check_current(self):
        for record in self:
            if record.is_current:
                other_current = self.search([
                    ('is_current', '=', True),
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id),
                ])
                if other_current:
                    raise ValidationError(
                        _('There can only be one current academic year!')
                    )
    def action_set_current(self):
        self.search([
            ('is_current', '=', True),
            ('company_id', '=', self.company_id.id),
        ]).write({'is_current': False})
        self.is_current = True
