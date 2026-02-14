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


class Exam(models.Model):
    _name = 'algorid.exam'
    _description = 'Exam'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char(
        string='Exam Name',
        required=True,
        tracking=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Exam Name (Bangla)',
    )
    code = fields.Char(
        string='Exam Code',
        required=True,
    )
    exam_type = fields.Selection([
        ('class_test', 'Class Test'),
        ('weekly', 'Weekly Test'),
        ('monthly', 'Monthly Test'),
        ('mid_term', 'Mid Term'),
        ('final', 'Final'),
        ('annual', 'Annual'),
    ], string='Exam Type', required=True, default='mid_term', tracking=True)
    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
        required=True,
        tracking=True,
    )
    class_ids = fields.Many2many(
        'algorid.class',
        'exam_class_rel',
        'exam_id',
        'class_id',
        string='Classes',
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
    schedule_ids = fields.One2many(
        'algorid.exam.schedule',
        'exam_id',
        string='Exam Schedule',
    )
    result_ids = fields.One2many(
        'algorid.exam.result',
        'exam_id',
        string='Results',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)
    weightage = fields.Float(
        string='Weightage (%)',
        default=100,
        help='Weightage of this exam in final result calculation',
    )
    pass_percentage = fields.Float(
        string='Pass Percentage',
        default=33.0,
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
    result_count = fields.Integer(
        string='Result Count',
        compute='_compute_result_count',
    )

    _sql_constraints = [
        ('code_unique', 'unique(code, academic_year_id, company_id)',
         'Exam code must be unique per academic year!'),
    ]

    @api.depends('result_ids')
    def _compute_result_count(self):
        for record in self:
            record.result_count = len(record.result_ids)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise ValidationError(_('End Date must be after Start Date!'))

    def action_schedule(self):
        """Schedule the exam."""
        self.write({'state': 'scheduled'})

    def action_start(self):
        """Start the exam."""
        self.write({'state': 'ongoing'})

    def action_complete(self):
        """Complete the exam."""
        self.write({'state': 'completed'})

    def action_publish(self):
        """Publish results."""
        self.write({'state': 'published'})

    def action_cancel(self):
        """Cancel the exam."""
        self.write({'state': 'cancelled'})

    def action_draft(self):
        """Reset to draft."""
        self.write({'state': 'draft'})

    def action_view_results(self):
        """View exam results."""
        self.ensure_one()
        return {
            'name': _('Exam Results'),
            'type': 'ir.actions.act_window',
            'res_model': 'algorid.exam.result',
            'view_mode': 'list,form',
            'domain': [('exam_id', '=', self.id)],
            'context': {'default_exam_id': self.id},
        }


class ExamSchedule(models.Model):
    _name = 'algorid.exam.schedule'
    _description = 'Exam Schedule'
    _order = 'date, start_time'

    exam_id = fields.Many2one(
        'algorid.exam',
        string='Exam',
        required=True,
        ondelete='cascade',
    )
    class_id = fields.Many2one(
        'algorid.class',
        string='Class',
        required=True,
    )
    subject_id = fields.Many2one(
        'algorid.subject',
        string='Subject',
        required=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
    )
    start_time = fields.Float(
        string='Start Time',
        required=True,
    )
    end_time = fields.Float(
        string='End Time',
        required=True,
    )
    room_no = fields.Char(
        string='Room No',
    )
    invigilator_id = fields.Many2one(
        'hr.employee',
        string='Invigilator',
        domain="[('is_teacher', '=', True)]",
    )
    full_marks = fields.Float(
        string='Full Marks',
        related='subject_id.full_marks',
        store=True,
    )
    pass_marks = fields.Float(
        string='Pass Marks',
        related='subject_id.pass_marks',
        store=True,
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

