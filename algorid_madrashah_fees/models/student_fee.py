# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class StudentFee(models.Model):
    _name = 'algorid.student.fee'
    _description = 'Student Fee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'due_date desc, student_id'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Name',
        compute='_compute_display_name',
        store=True,
    )
    student_id = fields.Many2one(
        'algorid.student',
        string='Student',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    fee_type_id = fields.Many2one(
        'algorid.fee.type',
        string='Fee Type',
        required=True,
        tracking=True,
    )
    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
        tracking=True,
    )
    class_id = fields.Many2one(
        'algorid.class',
        string='Class',
        related='student_id.class_id',
        store=True,
    )
    period_month = fields.Selection([
        ('01', 'January'), ('02', 'February'), ('03', 'March'),
        ('04', 'April'), ('05', 'May'), ('06', 'June'),
        ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ], string='Month')
    period_year = fields.Char(
        string='Year',
        size=4,
    )
    amount = fields.Float(
        string='Amount',
        required=True,
        tracking=True,
    )
    discount_id = fields.Many2one(
        'algorid.fee.discount',
        string='Discount',
    )
    discount_amount = fields.Float(
        string='Discount Amount',
        compute='_compute_amounts',
        store=True,
    )
    late_fee = fields.Float(
        string='Late Fee',
        compute='_compute_amounts',
        store=True,
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_amounts',
        store=True,
    )
    paid_amount = fields.Float(
        string='Paid Amount',
        tracking=True,
    )
    due_amount = fields.Float(
        string='Due Amount',
        compute='_compute_amounts',
        store=True,
    )
    due_date = fields.Date(
        string='Due Date',
        required=True,
        tracking=True,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        copy=False,
    )
    payment_ids = fields.One2many(
        'algorid.fee.payment',
        'student_fee_id',
        string='Payments',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    notes = fields.Text(
        string='Notes',
    )

    @api.depends('student_id', 'fee_type_id', 'period_month', 'period_year')
    def _compute_display_name(self):
        for record in self:
            parts = [record.student_id.name or '']
            if record.fee_type_id:
                parts.append(record.fee_type_id.name)
            if record.period_month and record.period_year:
                month_name = dict(record._fields['period_month'].selection).get(record.period_month, '')
                parts.append(f"{month_name} {record.period_year}")
            record.display_name = ' - '.join(filter(None, parts))

    @api.depends('amount', 'discount_id', 'due_date', 'paid_amount')
    def _compute_amounts(self):
        today = fields.Date.today()
        for record in self:
            # Calculate discount
            discount = 0
            if record.discount_id and record.amount:
                discount = record.discount_id.calculate_discount(record.amount)
            record.discount_amount = discount

            # Calculate late fee
            late_fee = 0
            if record.due_date and today > record.due_date and record.state not in ('paid', 'cancelled'):
                grace_days = int(self.env['ir.config_parameter'].sudo().get_param(
                    'algorid_madrashah.late_fee_grace_days', '10'
                ))
                late_fee_percentage = float(self.env['ir.config_parameter'].sudo().get_param(
                    'algorid_madrashah.late_fee_percentage', '5'
                ))

                days_late = (today - record.due_date).days
                if days_late > grace_days:
                    late_fee = (record.amount - discount) * (late_fee_percentage / 100)

            record.late_fee = late_fee
            record.total_amount = record.amount - discount + late_fee
            record.due_amount = record.total_amount - record.paid_amount

    def action_confirm(self):
        """Confirm the fee."""
        self.write({'state': 'pending'})

    def action_cancel(self):
        """Cancel the fee."""
        for record in self:
            if record.paid_amount > 0:
                raise UserError(_('Cannot cancel a fee with payments!'))
        self.write({'state': 'cancelled'})

    def action_draft(self):
        """Reset to draft."""
        self.write({'state': 'draft'})

    def action_create_invoice(self):
        """Create invoice for this fee."""
        self.ensure_one()
        if self.invoice_id:
            raise UserError(_('Invoice already exists!'))

        if not self.student_id.guardian_id:
            raise UserError(_('Student must have a guardian for invoicing!'))

        # Create or get partner for guardian
        partner = self.env['res.partner'].search([
            ('name', '=', self.student_id.guardian_id.name),
            ('email', '=', self.student_id.guardian_id.email),
        ], limit=1)

        if not partner:
            partner = self.env['res.partner'].create({
                'name': self.student_id.guardian_id.name,
                'email': self.student_id.guardian_id.email,
                'phone': self.student_id.guardian_id.phone,
                'mobile': self.student_id.guardian_id.mobile,
            })

        invoice_lines = [(0, 0, {
            'product_id': self.fee_type_id.product_id.id,
            'name': f"{self.fee_type_id.name} - {self.student_id.name}",
            'quantity': 1,
            'price_unit': self.amount,
        })]

        if self.discount_amount > 0:
            invoice_lines.append((0, 0, {
                'name': f"Discount: {self.discount_id.name}",
                'quantity': 1,
                'price_unit': -self.discount_amount,
            }))

        if self.late_fee > 0:
            invoice_lines.append((0, 0, {
                'name': "Late Fee",
                'quantity': 1,
                'price_unit': self.late_fee,
            }))

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': fields.Date.today(),
            'invoice_date_due': self.due_date,
            'invoice_line_ids': invoice_lines,
            'ref': f"Fee: {self.display_name}",
        })

        self.invoice_id = invoice.id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
        }

    def action_register_payment(self):
        """Open payment registration wizard."""
        self.ensure_one()
        return {
            'name': _('Register Payment'),
            'type': 'ir.actions.act_window',
            'res_model': 'algorid.fee.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_student_fee_id': self.id},
        }


class FeePayment(models.Model):
    _name = 'algorid.fee.payment'
    _description = 'Fee Payment'
    _order = 'payment_date desc'

    student_fee_id = fields.Many2one(
        'algorid.student.fee',
        string='Student Fee',
        required=True,
        ondelete='cascade',
    )
    payment_date = fields.Date(
        string='Payment Date',
        required=True,
        default=fields.Date.today,
    )
    amount = fields.Float(
        string='Amount',
        required=True,
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
    received_by = fields.Many2one(
        'res.users',
        string='Received By',
        default=lambda self: self.env.user,
    )
    notes = fields.Text(
        string='Notes',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # Update paid amount on student fee
            fee = record.student_fee_id
            fee.paid_amount = sum(fee.payment_ids.mapped('amount'))

            # Update state
            if fee.paid_amount >= fee.total_amount:
                fee.state = 'paid'
            elif fee.paid_amount > 0:
                fee.state = 'partial'

        return records

