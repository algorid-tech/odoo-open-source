# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _


class StudentDocument(models.Model):
    _name = 'algorid.student.document'
    _description = 'Student Document'
    _order = 'create_date desc'

    name = fields.Char(
        string='Document Name',
        required=True,
    )
    student_id = fields.Many2one(
        'algorid.student',
        string='Student',
        required=True,
        ondelete='cascade',
    )
    document_type = fields.Selection([
        ('birth_certificate', 'Birth Certificate'),
        ('photo', 'Photo'),
        ('previous_certificate', 'Previous School Certificate'),
        ('transfer_certificate', 'Transfer Certificate'),
        ('medical_certificate', 'Medical Certificate'),
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
        ('other', 'Other'),
    ], string='Document Type', required=True, default='other')
    file = fields.Binary(
        string='File',
        required=True,
        attachment=True,
    )
    file_name = fields.Char(
        string='File Name',
    )
    description = fields.Text(
        string='Description',
    )
    issue_date = fields.Date(
        string='Issue Date',
    )
    expiry_date = fields.Date(
        string='Expiry Date',
    )
    is_verified = fields.Boolean(
        string='Verified',
        default=False,
    )
    verified_by = fields.Many2one(
        'res.users',
        string='Verified By',
    )
    verified_date = fields.Date(
        string='Verified Date',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    def action_verify(self):
        """Verify the document."""
        self.write({
            'is_verified': True,
            'verified_by': self.env.user.id,
            'verified_date': fields.Date.today(),
        })

