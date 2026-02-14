# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################
from odoo import models, fields, api, _
class Subject(models.Model):
    _name = 'algorid.subject'
    _description = 'Subject'
    _order = 'sequence, name'
    name = fields.Char(
        string='Subject Name',
        required=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Subject Name (Bangla)',
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    subject_type = fields.Selection([
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('combined', 'Combined'),
    ], string='Subject Type', default='theory', required=True)
    credit_hours = fields.Float(
        string='Credit Hours',
        default=3.0,
    )
    weekly_hours = fields.Float(
        string='Weekly Hours',
        default=4.0,
    )
    full_marks = fields.Float(
        string='Full Marks',
        default=100.0,
    )
    pass_marks = fields.Float(
        string='Pass Marks',
        default=33.0,
    )
    is_optional = fields.Boolean(
        string='Optional Subject',
        default=False,
    )
    class_ids = fields.Many2many(
        'algorid.class',
        'class_subject_rel',
        'subject_id',
        'class_id',
        string='Classes',
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
         'Subject code must be unique!'),
    ]
