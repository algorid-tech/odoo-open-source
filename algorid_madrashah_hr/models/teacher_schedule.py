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


class TeacherSchedule(models.Model):
    _name = 'algorid.teacher.schedule'
    _description = 'Teacher Schedule'
    _order = 'day_of_week, start_time'

    teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        required=True,
        ondelete='cascade',
        domain="[('is_teacher', '=', True)]",
    )
    day_of_week = fields.Selection([
        ('0', 'Saturday'),
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
    ], string='Day', required=True)
    start_time = fields.Float(
        string='Start Time',
        required=True,
    )
    end_time = fields.Float(
        string='End Time',
        required=True,
    )
    class_id = fields.Many2one(
        'algorid.class',
        string='Class',
    )
    section_id = fields.Many2one(
        'algorid.section',
        string='Section',
        domain="[('class_id', '=', class_id)]",
    )
    subject_id = fields.Many2one(
        'algorid.subject',
        string='Subject',
    )
    room_no = fields.Char(
        string='Room No',
    )
    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
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

    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError(_('End time must be after start time!'))
            if record.start_time < 0 or record.start_time >= 24:
                raise ValidationError(_('Start time must be between 0 and 24!'))
            if record.end_time < 0 or record.end_time >= 24:
                raise ValidationError(_('End time must be between 0 and 24!'))

    @api.constrains('teacher_id', 'day_of_week', 'start_time', 'end_time')
    def _check_overlap(self):
        for record in self:
            overlapping = self.search([
                ('id', '!=', record.id),
                ('teacher_id', '=', record.teacher_id.id),
                ('day_of_week', '=', record.day_of_week),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time),
            ])
            if overlapping:
                raise ValidationError(
                    _('Teacher schedule overlaps with existing schedule!')
                )

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.section_id = False

