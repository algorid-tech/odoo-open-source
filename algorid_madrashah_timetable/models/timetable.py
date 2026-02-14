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


class Timetable(models.Model):
    _name = 'algorid.timetable'
    _description = 'Timetable'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'academic_year_id desc, class_id'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
    )
    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
        required=True,
        tracking=True,
    )
    class_id = fields.Many2one(
        'algorid.class',
        string='Class',
        required=True,
        tracking=True,
    )
    section_id = fields.Many2one(
        'algorid.section',
        string='Section',
        domain="[('class_id', '=', class_id)]",
        tracking=True,
    )
    line_ids = fields.One2many(
        'algorid.timetable.line',
        'timetable_id',
        string='Timetable Lines',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True)
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

    _sql_constraints = [
        ('unique_timetable', 'unique(academic_year_id, class_id, section_id, company_id)',
         'Timetable for this class/section already exists for this academic year!'),
    ]

    @api.depends('class_id', 'section_id', 'academic_year_id')
    def _compute_name(self):
        for record in self:
            parts = []
            if record.class_id:
                parts.append(record.class_id.name)
            if record.section_id:
                parts.append(record.section_id.name)
            if record.academic_year_id:
                parts.append(record.academic_year_id.name)
            record.name = ' - '.join(parts) if parts else 'New Timetable'

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.section_id = False

    def action_activate(self):
        """Activate the timetable."""
        self.write({'state': 'active'})

    def action_archive(self):
        """Archive the timetable."""
        self.write({'state': 'archived'})

    def action_draft(self):
        """Reset to draft."""
        self.write({'state': 'draft'})

    def action_check_conflicts(self):
        """Check for scheduling conflicts."""
        self.ensure_one()
        conflicts = []

        for line in self.line_ids:
            # Check teacher conflict
            teacher_conflict = self.env['algorid.timetable.line'].search([
                ('id', '!=', line.id),
                ('timetable_id.state', '=', 'active'),
                ('teacher_id', '=', line.teacher_id.id),
                ('day_of_week', '=', line.day_of_week),
                ('period_id', '=', line.period_id.id),
            ])

            if teacher_conflict:
                conflicts.append(
                    _("Teacher %s has conflict on %s during %s") % (
                        line.teacher_id.name,
                        dict(line._fields['day_of_week'].selection).get(line.day_of_week),
                        line.period_id.name,
                    )
                )

            # Check room conflict
            if line.room_no:
                room_conflict = self.env['algorid.timetable.line'].search([
                    ('id', '!=', line.id),
                    ('timetable_id.state', '=', 'active'),
                    ('room_no', '=', line.room_no),
                    ('day_of_week', '=', line.day_of_week),
                    ('period_id', '=', line.period_id.id),
                ])

                if room_conflict:
                    conflicts.append(
                        _("Room %s has conflict on %s during %s") % (
                            line.room_no,
                            dict(line._fields['day_of_week'].selection).get(line.day_of_week),
                            line.period_id.name,
                        )
                    )

        if conflicts:
            raise ValidationError('\n'.join(conflicts))

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('No conflicts found!'),
                'type': 'success',
            }
        }


class TimetableLine(models.Model):
    _name = 'algorid.timetable.line'
    _description = 'Timetable Line'
    _order = 'day_of_week, period_id'

    timetable_id = fields.Many2one(
        'algorid.timetable',
        string='Timetable',
        required=True,
        ondelete='cascade',
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
    period_id = fields.Many2one(
        'algorid.period',
        string='Period',
        required=True,
        domain="[('period_type', '=', 'class')]",
    )
    subject_id = fields.Many2one(
        'algorid.subject',
        string='Subject',
        required=True,
    )
    teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        domain="[('is_teacher', '=', True)]",
    )
    room_no = fields.Char(
        string='Room No',
    )
    start_time = fields.Float(
        string='Start Time',
        related='period_id.start_time',
        store=True,
    )
    end_time = fields.Float(
        string='End Time',
        related='period_id.end_time',
        store=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='timetable_id.company_id',
        store=True,
    )

    @api.constrains('timetable_id', 'day_of_week', 'period_id')
    def _check_duplicate(self):
        for record in self:
            duplicate = self.search([
                ('id', '!=', record.id),
                ('timetable_id', '=', record.timetable_id.id),
                ('day_of_week', '=', record.day_of_week),
                ('period_id', '=', record.period_id.id),
            ])
            if duplicate:
                raise ValidationError(
                    _('This time slot is already assigned for %s!') %
                    dict(record._fields['day_of_week'].selection).get(record.day_of_week)
                )

