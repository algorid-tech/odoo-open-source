# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################
from odoo import models, fields, api, _
class MadrasahClass(models.Model):
    _name = 'algorid.class'
    _description = 'Class'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    name = fields.Char(
        string='Class Name',
        required=True,
        tracking=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Class Name (Bangla)',
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    section_ids = fields.One2many(
        'algorid.section',
        'class_id',
        string='Sections',
    )
    subject_ids = fields.Many2many(
        'algorid.subject',
        'class_subject_rel',
        'class_id',
        'subject_id',
        string='Subjects',
    )
    capacity = fields.Integer(
        string='Capacity',
        default=40,
    )
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_student_count',
    )
    class_teacher_id = fields.Many2one(
        'hr.employee',
        string='Class Teacher',
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
         'Class code must be unique!'),
    ]
    def _compute_student_count(self):
        for record in self:
            record.student_count = 0
