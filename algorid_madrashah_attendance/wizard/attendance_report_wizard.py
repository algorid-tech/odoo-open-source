# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

import base64
import csv
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AttendanceReportWizard(models.TransientModel):
    _name = 'algorid.attendance.report.wizard'
    _description = 'Attendance Report Wizard'

    report_type = fields.Selection([
        ('student', 'Student Attendance'),
        ('teacher', 'Teacher Attendance'),
    ], string='Report Type', required=True, default='student')

    date_from = fields.Date(
        string='From Date',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1),
    )
    date_to = fields.Date(
        string='To Date',
        required=True,
        default=fields.Date.today,
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
    student_id = fields.Many2one(
        'algorid.student',
        string='Student',
    )
    teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        domain="[('is_teacher', '=', True)]",
    )
    export_format = fields.Selection([
        ('view', 'View Report'),
        ('csv', 'Export CSV'),
    ], string='Output', default='view', required=True)

    # CSV Export fields
    csv_file = fields.Binary(string='CSV File', readonly=True)
    csv_filename = fields.Char(string='Filename', readonly=True)

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.section_id = False
        self.student_id = False

    def action_generate_report(self):
        self.ensure_one()

        if self.export_format == 'csv':
            return self._export_csv()
        else:
            return self._view_report()

    def _view_report(self):
        """View attendance report."""
        if self.report_type == 'student':
            domain = [
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
            ]
            if self.class_id:
                domain.append(('class_id', '=', self.class_id.id))
            if self.section_id:
                domain.append(('section_id', '=', self.section_id.id))
            if self.student_id:
                domain.append(('student_id', '=', self.student_id.id))

            return {
                'name': _('Student Attendance Report'),
                'type': 'ir.actions.act_window',
                'res_model': 'algorid.student.attendance',
                'view_mode': 'list,form',
                'domain': domain,
                'context': {'search_default_group_student': 1},
            }
        else:
            domain = [
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
            ]
            if self.teacher_id:
                domain.append(('employee_id', '=', self.teacher_id.id))

            return {
                'name': _('Teacher Attendance Report'),
                'type': 'ir.actions.act_window',
                'res_model': 'algorid.teacher.attendance',
                'view_mode': 'list,form',
                'domain': domain,
                'context': {'search_default_group_teacher': 1},
            }

    def _export_csv(self):
        """Export attendance to CSV."""
        output = StringIO()
        writer = csv.writer(output)

        if self.report_type == 'student':
            writer.writerow([
                'Student ID', 'Student Name', 'Class', 'Section',
                'Date', 'Status', 'Remarks'
            ])

            domain = [
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
            ]
            if self.class_id:
                domain.append(('class_id', '=', self.class_id.id))
            if self.section_id:
                domain.append(('section_id', '=', self.section_id.id))
            if self.student_id:
                domain.append(('student_id', '=', self.student_id.id))

            records = self.env['algorid.student.attendance'].search(domain, order='date, student_id')

            for rec in records:
                writer.writerow([
                    rec.student_id.student_id,
                    rec.student_id.name,
                    rec.class_id.name,
                    rec.section_id.name or '',
                    rec.date,
                    dict(rec._fields['status'].selection).get(rec.status),
                    rec.remarks or '',
                ])

            filename = f'student_attendance_{self.date_from}_{self.date_to}.csv'
        else:
            writer.writerow([
                'Teacher ID', 'Teacher Name', 'Date', 'Status',
                'Check In', 'Check Out', 'Worked Hours', 'Remarks'
            ])

            domain = [
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
            ]
            if self.teacher_id:
                domain.append(('employee_id', '=', self.teacher_id.id))

            records = self.env['algorid.teacher.attendance'].search(domain, order='date, employee_id')

            for rec in records:
                writer.writerow([
                    rec.employee_id.teacher_id or '',
                    rec.employee_id.name,
                    rec.date,
                    dict(rec._fields['status'].selection).get(rec.status),
                    rec.check_in_time,
                    rec.check_out_time,
                    rec.worked_hours,
                    rec.remarks or '',
                ])

            filename = f'teacher_attendance_{self.date_from}_{self.date_to}.csv'

        csv_content = output.getvalue()
        output.close()

        self.csv_file = base64.b64encode(csv_content.encode('utf-8'))
        self.csv_filename = filename

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'algorid.attendance.report.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': {'download': True},
        }

