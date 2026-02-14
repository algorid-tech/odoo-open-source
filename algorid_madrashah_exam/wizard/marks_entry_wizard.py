# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MarksEntryWizard(models.TransientModel):
    _name = 'algorid.marks.entry.wizard'
    _description = 'Marks Entry Wizard'

    exam_id = fields.Many2one(
        'algorid.exam',
        string='Exam',
        required=True,
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
    subject_id = fields.Many2one(
        'algorid.subject',
        string='Subject',
        required=True,
    )
    line_ids = fields.One2many(
        'algorid.marks.entry.wizard.line',
        'wizard_id',
        string='Marks Entry',
    )

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.section_id = False
        self.line_ids = False

    @api.onchange('exam_id', 'class_id', 'section_id', 'subject_id')
    def _onchange_filters(self):
        if not all([self.exam_id, self.class_id, self.subject_id]):
            return

        domain = [
            ('class_id', '=', self.class_id.id),
            ('state', '=', 'active'),
        ]
        if self.section_id:
            domain.append(('section_id', '=', self.section_id.id))

        students = self.env['algorid.student'].search(domain, order='roll_no, name')

        lines = []
        for student in students:
            # Check for existing result
            existing_result = self.env['algorid.exam.result'].search([
                ('exam_id', '=', self.exam_id.id),
                ('student_id', '=', student.id),
            ], limit=1)

            existing_marks = 0
            if existing_result:
                existing_line = existing_result.line_ids.filtered(
                    lambda l: l.subject_id.id == self.subject_id.id
                )
                if existing_line:
                    existing_marks = existing_line[0].marks_obtained

            lines.append((0, 0, {
                'student_id': student.id,
                'roll_no': student.roll_no,
                'marks_obtained': existing_marks,
            }))

        self.line_ids = lines

    def action_save_marks(self):
        """Save marks for all students."""
        self.ensure_one()

        for line in self.line_ids:
            # Get or create result
            result = self.env['algorid.exam.result'].search([
                ('exam_id', '=', self.exam_id.id),
                ('student_id', '=', line.student_id.id),
            ], limit=1)

            if not result:
                result = self.env['algorid.exam.result'].create({
                    'exam_id': self.exam_id.id,
                    'student_id': line.student_id.id,
                })

            # Get or create result line
            result_line = result.line_ids.filtered(
                lambda l: l.subject_id.id == self.subject_id.id
            )

            if result_line:
                result_line.write({'marks_obtained': line.marks_obtained})
            else:
                self.env['algorid.exam.result.line'].create({
                    'result_id': result.id,
                    'subject_id': self.subject_id.id,
                    'marks_obtained': line.marks_obtained,
                })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Marks saved successfully!'),
                'type': 'success',
            }
        }


class MarksEntryWizardLine(models.TransientModel):
    _name = 'algorid.marks.entry.wizard.line'
    _description = 'Marks Entry Wizard Line'
    _order = 'roll_no, student_id'

    wizard_id = fields.Many2one(
        'algorid.marks.entry.wizard',
        string='Wizard',
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
    )
    marks_obtained = fields.Float(
        string='Marks Obtained',
    )

