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
from dateutil.relativedelta import relativedelta


class FeeInvoiceWizard(models.TransientModel):
    _name = 'algorid.fee.invoice.wizard'
    _description = 'Fee Invoice Generation Wizard'

    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
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
    student_ids = fields.Many2many(
        'algorid.student',
        string='Students',
        domain="[('state', '=', 'active')]",
    )
    fee_type_ids = fields.Many2many(
        'algorid.fee.type',
        string='Fee Types',
        required=True,
    )
    period_month = fields.Selection([
        ('01', 'January'), ('02', 'February'), ('03', 'March'),
        ('04', 'April'), ('05', 'May'), ('06', 'June'),
        ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ], string='Month', required=True)
    period_year = fields.Char(
        string='Year',
        size=4,
        required=True,
        default=lambda self: str(fields.Date.today().year),
    )
    due_date = fields.Date(
        string='Due Date',
        required=True,
        default=lambda self: fields.Date.today() + relativedelta(days=10),
    )

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.section_id = False
        self.student_ids = False

    @api.onchange('class_id', 'section_id')
    def _onchange_filters(self):
        domain = [('state', '=', 'active')]
        if self.class_id:
            domain.append(('class_id', '=', self.class_id.id))
        if self.section_id:
            domain.append(('section_id', '=', self.section_id.id))

        students = self.env['algorid.student'].search(domain)
        self.student_ids = students

    def action_generate_fees(self):
        """Generate fee records for selected students."""
        self.ensure_one()

        if not self.student_ids:
            raise UserError(_('Please select at least one student!'))

        created_fees = self.env['algorid.student.fee']

        for student in self.student_ids:
            # Get fee structure for this class
            structure = self.env['algorid.fee.structure'].search([
                ('academic_year_id', '=', self.academic_year_id.id),
                ('class_id', '=', student.class_id.id),
            ], limit=1)

            for fee_type in self.fee_type_ids:
                # Check if fee already exists
                existing = self.env['algorid.student.fee'].search([
                    ('student_id', '=', student.id),
                    ('fee_type_id', '=', fee_type.id),
                    ('period_month', '=', self.period_month),
                    ('period_year', '=', self.period_year),
                ], limit=1)

                if existing:
                    continue

                # Get amount from structure or default
                amount = fee_type.default_amount
                if structure:
                    line = structure.line_ids.filtered(lambda l: l.fee_type_id == fee_type)
                    if line:
                        amount = line[0].amount

                # Get applicable discount
                discount = False
                if 'scholarship' in student.tag_ids.mapped('name'):
                    discount = self.env['algorid.fee.discount'].search([
                        ('eligibility', '=', 'scholarship'),
                        ('active', '=', True),
                    ], limit=1)

                fee = self.env['algorid.student.fee'].create({
                    'student_id': student.id,
                    'fee_type_id': fee_type.id,
                    'academic_year_id': self.academic_year_id.id,
                    'period_month': self.period_month,
                    'period_year': self.period_year,
                    'amount': amount,
                    'discount_id': discount.id if discount else False,
                    'due_date': self.due_date,
                    'state': 'pending',
                })
                created_fees |= fee

        return {
            'name': _('Generated Fees'),
            'type': 'ir.actions.act_window',
            'res_model': 'algorid.student.fee',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created_fees.ids)],
        }


class FeePaymentWizard(models.TransientModel):
    _name = 'algorid.fee.payment.wizard'
    _description = 'Fee Payment Wizard'

    student_fee_id = fields.Many2one(
        'algorid.student.fee',
        string='Student Fee',
        required=True,
    )
    due_amount = fields.Float(
        string='Due Amount',
        related='student_fee_id.due_amount',
    )
    amount = fields.Float(
        string='Payment Amount',
        required=True,
    )
    payment_date = fields.Date(
        string='Payment Date',
        required=True,
        default=fields.Date.today,
    )
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('online', 'Online Payment'),
        ('mobile', 'Mobile Banking'),
    ], string='Payment Method', required=True, default='cash')
    reference = fields.Char(
        string='Reference',
    )
    notes = fields.Text(
        string='Notes',
    )

    @api.onchange('student_fee_id')
    def _onchange_student_fee_id(self):
        if self.student_fee_id:
            self.amount = self.student_fee_id.due_amount

    def action_register_payment(self):
        """Register the payment."""
        self.ensure_one()

        if self.amount <= 0:
            raise UserError(_('Payment amount must be positive!'))

        self.env['algorid.fee.payment'].create({
            'student_fee_id': self.student_fee_id.id,
            'payment_date': self.payment_date,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'reference': self.reference,
            'notes': self.notes,
        })

        return {'type': 'ir.actions.act_window_close'}

