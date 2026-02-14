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


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Teacher specific fields
    is_teacher = fields.Boolean(
        string='Is Teacher',
        default=False,
    )
    teacher_id = fields.Char(
        string='Teacher ID',
        copy=False,
    )
    name_bn = fields.Char(
        string='Name (Bangla)',
    )

    # Qualifications
    qualification_ids = fields.One2many(
        'algorid.teacher.qualification',
        'employee_id',
        string='Qualifications',
    )
    highest_qualification = fields.Char(
        string='Highest Qualification',
    )
    specialization = fields.Char(
        string='Specialization',
    )

    # Teaching Information
    subject_ids = fields.Many2many(
        'algorid.subject',
        'employee_subject_rel',
        'employee_id',
        'subject_id',
        string='Subjects',
    )
    class_ids = fields.Many2many(
        'algorid.class',
        'employee_class_rel',
        'employee_id',
        'class_id',
        string='Assigned Classes',
    )
    section_ids = fields.Many2many(
        'algorid.section',
        'employee_section_rel',
        'employee_id',
        'section_id',
        string='Class Teacher Of',
    )

    # Schedule
    schedule_ids = fields.One2many(
        'algorid.teacher.schedule',
        'teacher_id',
        string='Schedules',
    )

    # Experience
    total_experience_years = fields.Float(
        string='Total Experience (Years)',
    )
    date_of_joining = fields.Date(
        string='Date of Joining',
    )

    # Additional Information
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('other', 'Other'),
    ], string='Religion', default='islam')
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string='Blood Group')
    national_id = fields.Char(
        string='National ID',
    )

    # Emergency Contact
    emergency_contact_name = fields.Char(
        string='Emergency Contact Name',
    )
    emergency_contact_phone = fields.Char(
        string='Emergency Contact Phone',
    )
    emergency_contact_relation = fields.Char(
        string='Relation',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_teacher') and not vals.get('teacher_id'):
                vals['teacher_id'] = self.env['ir.sequence'].next_by_code(
                    'algorid.teacher'
                ) or 'TCH/'
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('is_teacher'):
            for record in self:
                if not record.teacher_id:
                    vals['teacher_id'] = self.env['ir.sequence'].next_by_code(
                        'algorid.teacher'
                    ) or 'TCH/'
        return super().write(vals)


class TeacherQualification(models.Model):
    _name = 'algorid.teacher.qualification'
    _description = 'Teacher Qualification'
    _order = 'year desc'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(
        string='Degree/Certificate',
        required=True,
    )
    institution = fields.Char(
        string='Institution',
        required=True,
    )
    board_university = fields.Char(
        string='Board/University',
    )
    year = fields.Char(
        string='Year',
    )
    result = fields.Char(
        string='Result/Grade',
    )
    subject = fields.Char(
        string='Major Subject',
    )
    certificate = fields.Binary(
        string='Certificate',
        attachment=True,
    )
    certificate_name = fields.Char(
        string='Certificate Filename',
    )

