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


class GradeConfig(models.Model):
    _name = 'algorid.grade.config'
    _description = 'Grade Configuration'
    _order = 'min_percentage desc'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
    )
    grade = fields.Char(
        string='Grade',
        required=True,
    )
    grade_bn = fields.Char(
        string='Grade (Bangla)',
    )
    min_percentage = fields.Float(
        string='Minimum Percentage',
        required=True,
    )
    max_percentage = fields.Float(
        string='Maximum Percentage',
        required=True,
    )
    grade_point = fields.Float(
        string='Grade Point',
        required=True,
    )
    min_gpa = fields.Float(
        string='Minimum GPA',
    )
    max_gpa = fields.Float(
        string='Maximum GPA',
    )
    description = fields.Char(
        string='Description',
        translate=True,
    )
    description_bn = fields.Char(
        string='Description (Bangla)',
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

    @api.depends('grade', 'min_percentage', 'max_percentage')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.grade} ({record.min_percentage}% - {record.max_percentage}%)"

    @api.constrains('min_percentage', 'max_percentage')
    def _check_percentage(self):
        for record in self:
            if record.min_percentage < 0 or record.max_percentage < 0:
                raise ValidationError(_('Percentage cannot be negative!'))
            if record.min_percentage > record.max_percentage:
                raise ValidationError(_('Minimum percentage cannot exceed maximum!'))
            if record.max_percentage > 100:
                raise ValidationError(_('Percentage cannot exceed 100!'))

    @api.constrains('grade_point')
    def _check_grade_point(self):
        for record in self:
            if record.grade_point < 0:
                raise ValidationError(_('Grade point cannot be negative!'))
            if record.grade_point > 5:
                raise ValidationError(_('Grade point cannot exceed 5.0!'))

