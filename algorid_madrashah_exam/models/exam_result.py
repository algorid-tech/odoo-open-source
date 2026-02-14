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


class ExamResult(models.Model):
    _name = 'algorid.exam.result'
    _description = 'Exam Result'
    _inherit = ['mail.thread']
    _order = 'exam_id, student_id'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Name',
        compute='_compute_display_name',
        store=True,
    )
    exam_id = fields.Many2one(
        'algorid.exam',
        string='Exam',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    student_id = fields.Many2one(
        'algorid.student',
        string='Student',
        required=True,
        tracking=True,
    )
    class_id = fields.Many2one(
        'algorid.class',
        string='Class',
        related='student_id.class_id',
        store=True,
    )
    section_id = fields.Many2one(
        'algorid.section',
        string='Section',
        related='student_id.section_id',
        store=True,
    )
    roll_no = fields.Integer(
        string='Roll No',
        related='student_id.roll_no',
        store=True,
    )
    line_ids = fields.One2many(
        'algorid.exam.result.line',
        'result_id',
        string='Subject Results',
    )
    total_marks = fields.Float(
        string='Total Marks Obtained',
        compute='_compute_totals',
        store=True,
    )
    total_full_marks = fields.Float(
        string='Total Full Marks',
        compute='_compute_totals',
        store=True,
    )
    percentage = fields.Float(
        string='Percentage',
        compute='_compute_totals',
        store=True,
    )
    gpa = fields.Float(
        string='GPA',
        compute='_compute_totals',
        store=True,
        digits=(3, 2),
    )
    grade = fields.Char(
        string='Grade',
        compute='_compute_totals',
        store=True,
    )
    rank = fields.Integer(
        string='Class Rank',
    )
    is_passed = fields.Boolean(
        string='Passed',
        compute='_compute_totals',
        store=True,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('published', 'Published'),
    ], string='Status', default='draft', tracking=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    remarks = fields.Text(
        string='Remarks',
    )

    _sql_constraints = [
        ('unique_result', 'unique(exam_id, student_id)',
         'Result for this student in this exam already exists!'),
    ]

    @api.depends('student_id', 'exam_id')
    def _compute_display_name(self):
        for record in self:
            if record.student_id and record.exam_id:
                record.display_name = f"{record.student_id.name} - {record.exam_id.name}"
            else:
                record.display_name = "New Result"

    @api.depends('line_ids', 'line_ids.marks_obtained', 'line_ids.full_marks', 'line_ids.grade_point')
    def _compute_totals(self):
        for record in self:
            total_marks = sum(record.line_ids.mapped('marks_obtained'))
            total_full = sum(record.line_ids.mapped('full_marks'))

            record.total_marks = total_marks
            record.total_full_marks = total_full

            if total_full > 0:
                record.percentage = (total_marks / total_full) * 100
            else:
                record.percentage = 0

            # Calculate GPA
            total_credits = sum(record.line_ids.mapped('credit_hours'))
            if total_credits > 0:
                weighted_gpa = sum(
                    line.grade_point * line.credit_hours
                    for line in record.line_ids
                )
                record.gpa = weighted_gpa / total_credits
            else:
                # Simple average if no credit hours
                if record.line_ids:
                    record.gpa = sum(record.line_ids.mapped('grade_point')) / len(record.line_ids)
                else:
                    record.gpa = 0

            # Get overall grade from GPA
            grade_config = self.env['algorid.grade.config'].search([
                ('min_gpa', '<=', record.gpa),
                ('max_gpa', '>=', record.gpa),
            ], limit=1)
            record.grade = grade_config.grade if grade_config else ''

            # Check if passed
            failed_subjects = record.line_ids.filtered(lambda l: not l.is_passed)
            record.is_passed = len(failed_subjects) == 0 and len(record.line_ids) > 0

    def action_confirm(self):
        """Confirm the result."""
        self.write({'state': 'confirmed'})

    def action_publish(self):
        """Publish the result."""
        self.write({'state': 'published'})

    def action_draft(self):
        """Reset to draft."""
        self.write({'state': 'draft'})

    def action_print_report_card(self):
        """Print report card."""
        return self.env.ref('algorid_madrashah_exam.action_report_card').report_action(self)


class ExamResultLine(models.Model):
    _name = 'algorid.exam.result.line'
    _description = 'Exam Result Line'
    _order = 'subject_id'

    result_id = fields.Many2one(
        'algorid.exam.result',
        string='Result',
        required=True,
        ondelete='cascade',
    )
    subject_id = fields.Many2one(
        'algorid.subject',
        string='Subject',
        required=True,
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
    credit_hours = fields.Float(
        string='Credit Hours',
        related='subject_id.credit_hours',
        store=True,
    )
    marks_obtained = fields.Float(
        string='Marks Obtained',
    )
    percentage = fields.Float(
        string='Percentage',
        compute='_compute_grade',
        store=True,
    )
    grade = fields.Char(
        string='Grade',
        compute='_compute_grade',
        store=True,
    )
    grade_point = fields.Float(
        string='Grade Point',
        compute='_compute_grade',
        store=True,
    )
    is_passed = fields.Boolean(
        string='Passed',
        compute='_compute_grade',
        store=True,
    )
    remarks = fields.Char(
        string='Remarks',
    )

    @api.depends('marks_obtained', 'full_marks', 'pass_marks')
    def _compute_grade(self):
        for record in self:
            if record.full_marks > 0:
                record.percentage = (record.marks_obtained / record.full_marks) * 100
            else:
                record.percentage = 0

            record.is_passed = record.marks_obtained >= record.pass_marks

            # Get grade from configuration
            grade_config = self.env['algorid.grade.config'].search([
                ('min_percentage', '<=', record.percentage),
                ('max_percentage', '>=', record.percentage),
            ], limit=1)

            if grade_config:
                record.grade = grade_config.grade
                record.grade_point = grade_config.grade_point
            else:
                record.grade = 'F'
                record.grade_point = 0.0

    @api.constrains('marks_obtained', 'full_marks')
    def _check_marks(self):
        for record in self:
            if record.marks_obtained < 0:
                raise ValidationError(_('Marks cannot be negative!'))
            if record.marks_obtained > record.full_marks:
                raise ValidationError(
                    _('Marks obtained cannot exceed full marks for %s!') % record.subject_id.name
                )

