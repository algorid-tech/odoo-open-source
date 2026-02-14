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


class TeacherAttendance(models.Model):
    _name = 'algorid.teacher.attendance'
    _description = 'Teacher Attendance'
    _inherit = ['mail.thread']
    _order = 'date desc, employee_id'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        required=True,
        ondelete='cascade',
        domain="[('is_teacher', '=', True)]",
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
        ('half_day', 'Half Day'),
        ('on_leave', 'On Leave'),
    ], string='Status', required=True, default='present', tracking=True)
    check_in_time = fields.Float(
        string='Check In Time',
    )
    check_out_time = fields.Float(
        string='Check Out Time',
    )
    worked_hours = fields.Float(
        string='Worked Hours',
        compute='_compute_worked_hours',
        store=True,
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
        ('unique_attendance', 'unique(employee_id, date)',
         'Attendance for this teacher on this date already exists!'),
    ]

    @api.depends('check_in_time', 'check_out_time')
    def _compute_worked_hours(self):
        for record in self:
            if record.check_in_time and record.check_out_time:
                record.worked_hours = record.check_out_time - record.check_in_time
            else:
                record.worked_hours = 0

    @api.constrains('check_in_time', 'check_out_time')
    def _check_times(self):
        for record in self:
            if record.check_in_time and record.check_out_time:
                if record.check_in_time >= record.check_out_time:
                    raise ValidationError(_('Check out time must be after check in time!'))

    @api.model
    def get_attendance_summary(self, employee_id, start_date, end_date):
        """Get attendance summary for a teacher within date range."""
        domain = [
            ('employee_id', '=', employee_id),
            ('date', '>=', start_date),
            ('date', '<=', end_date),
        ]
        attendances = self.search(domain)

        summary = {
            'total_days': len(attendances),
            'present': len(attendances.filtered(lambda a: a.status == 'present')),
            'absent': len(attendances.filtered(lambda a: a.status == 'absent')),
            'late': len(attendances.filtered(lambda a: a.status == 'late')),
            'on_leave': len(attendances.filtered(lambda a: a.status == 'on_leave')),
            'half_day': len(attendances.filtered(lambda a: a.status == 'half_day')),
            'total_worked_hours': sum(attendances.mapped('worked_hours')),
        }

        if summary['total_days'] > 0:
            summary['attendance_percentage'] = (
                (summary['present'] + summary['late'] + summary['half_day'] * 0.5)
                / summary['total_days'] * 100
            )
        else:
            summary['attendance_percentage'] = 0

        return summary

