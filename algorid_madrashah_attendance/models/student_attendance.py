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


class StudentAttendance(models.Model):
    _name = 'algorid.student.attendance'
    _description = 'Student Attendance'
    _inherit = ['mail.thread']
    _order = 'date desc, student_id'
    _rec_name = 'student_id'

    student_id = fields.Many2one(
        'algorid.student',
        string='Student',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
        ('half_day', 'Half Day'),
    ], string='Status', required=True, default='present', tracking=True)
    check_in_time = fields.Float(
        string='Check In Time',
    )
    check_out_time = fields.Float(
        string='Check Out Time',
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
    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
    )
    remarks = fields.Text(
        string='Remarks',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        ('unique_attendance', 'unique(student_id, date)',
         'Attendance for this student on this date already exists!'),
    ]

    @api.model
    def get_attendance_summary(self, student_id, start_date, end_date):
        """Get attendance summary for a student within date range."""
        domain = [
            ('student_id', '=', student_id),
            ('date', '>=', start_date),
            ('date', '<=', end_date),
        ]
        attendances = self.search(domain)

        summary = {
            'total_days': len(attendances),
            'present': len(attendances.filtered(lambda a: a.status == 'present')),
            'absent': len(attendances.filtered(lambda a: a.status == 'absent')),
            'late': len(attendances.filtered(lambda a: a.status == 'late')),
            'excused': len(attendances.filtered(lambda a: a.status == 'excused')),
            'half_day': len(attendances.filtered(lambda a: a.status == 'half_day')),
        }

        if summary['total_days'] > 0:
            summary['attendance_percentage'] = (
                (summary['present'] + summary['late'] + summary['half_day'] * 0.5)
                / summary['total_days'] * 100
            )
        else:
            summary['attendance_percentage'] = 0

        return summary


class StudentAttendanceSheet(models.Model):
    _name = 'algorid.attendance.sheet'
    _description = 'Attendance Sheet'
    _order = 'date desc'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
    )
    class_id = fields.Many2one(
        'algorid.class',
        string='Class',
        required=True,
    )
    section_id = fields.Many2one(
        'algorid.section',
        string='Section',
        domain="[('class_id', '=', class_id)]",
    )
    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='draft')
    line_ids = fields.One2many(
        'algorid.attendance.sheet.line',
        'sheet_id',
        string='Attendance Lines',
    )
    total_students = fields.Integer(
        string='Total Students',
        compute='_compute_totals',
        store=True,
    )
    present_count = fields.Integer(
        string='Present',
        compute='_compute_totals',
        store=True,
    )
    absent_count = fields.Integer(
        string='Absent',
        compute='_compute_totals',
        store=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    @api.depends('class_id', 'section_id', 'date')
    def _compute_name(self):
        for record in self:
            section = record.section_id.name if record.section_id else ''
            record.name = f"Attendance - {record.class_id.name} {section} - {record.date}"

    @api.depends('line_ids', 'line_ids.status')
    def _compute_totals(self):
        for record in self:
            record.total_students = len(record.line_ids)
            record.present_count = len(record.line_ids.filtered(
                lambda l: l.status in ('present', 'late')
            ))
            record.absent_count = len(record.line_ids.filtered(
                lambda l: l.status == 'absent'
            ))

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.section_id = False
        self.line_ids = False

    def action_load_students(self):
        """Load students for the selected class/section."""
        self.ensure_one()
        self.line_ids.unlink()

        domain = [
            ('class_id', '=', self.class_id.id),
            ('state', '=', 'active'),
        ]
        if self.section_id:
            domain.append(('section_id', '=', self.section_id.id))

        students = self.env['algorid.student'].search(domain, order='roll_no, name')

        lines = []
        for student in students:
            lines.append((0, 0, {
                'student_id': student.id,
                'status': 'present',
            }))

        self.line_ids = lines

    def action_confirm(self):
        """Confirm and create attendance records."""
        self.ensure_one()

        for line in self.line_ids:
            existing = self.env['algorid.student.attendance'].search([
                ('student_id', '=', line.student_id.id),
                ('date', '=', self.date),
            ])
            if existing:
                existing.write({'status': line.status, 'remarks': line.remarks})
            else:
                self.env['algorid.student.attendance'].create({
                    'student_id': line.student_id.id,
                    'date': self.date,
                    'status': line.status,
                    'academic_year_id': self.academic_year_id.id,
                    'remarks': line.remarks,
                })

        self.state = 'confirmed'

    def action_draft(self):
        """Reset to draft."""
        self.state = 'draft'


class AttendanceSheetLine(models.Model):
    _name = 'algorid.attendance.sheet.line'
    _description = 'Attendance Sheet Line'
    _order = 'roll_no, student_id'

    sheet_id = fields.Many2one(
        'algorid.attendance.sheet',
        string='Attendance Sheet',
        required=True,
        ondelete='cascade',
    )
    student_id = fields.Many2one(
        'algorid.student',
        string='Student',
        required=True,
    )
    roll_no = fields.Integer(
        string='Roll No',
        related='student_id.roll_no',
        store=True,
    )
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
        ('half_day', 'Half Day'),
    ], string='Status', required=True, default='present')
    remarks = fields.Char(
        string='Remarks',
    )

