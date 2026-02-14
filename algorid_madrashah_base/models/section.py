# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################
from odoo import models, fields, api, _
class Section(models.Model):
    _name = 'algorid.section'
    _description = 'Section'
    _order = 'class_id, name'
    name = fields.Char(
        string='Section Name',
        required=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Section Name (Bangla)',
    )
    code = fields.Char(
        string='Code',
    )
    class_id = fields.Many2one(
        'algorid.class',
        string='Class',
        required=True,
        ondelete='cascade',
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
    room_no = fields.Char(
        string='Room No',
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
    _sql_constraints = [
        ('unique_section', 'unique(name, class_id, company_id)', 
         'Section name must be unique per class!'),
    ]
    def _compute_student_count(self):
        for record in self:
            record.student_count = 0
