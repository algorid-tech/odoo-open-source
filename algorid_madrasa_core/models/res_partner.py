# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2025 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """Inherits from res.partner to add student and guardian management features."""
    _inherit = 'res.partner'

    student_code = fields.Char(string='Student Code', copy=False, default=lambda self: _('New'),
                               help='Unique code for the student, used for identification purposes.')
    is_student = fields.Boolean(string='Is Student', default=False, help='Indicates if this partner is a student.')
    contact_type = fields.Selection(string='Contact Type', selection=[('student', 'Student'), ('guardian', 'Guardian')],
                                    compute='_compute_contact_type', inverse='_write_contact_type')
    guardian_id = fields.Many2one('res.partner', string='Guardian', domain="[('is_student', '=', False)]",
                                  help='The guardian of the student. This field is only applicable if the partner is a student.')

    @api.depends('is_student')
    def _compute_contact_type(self):
        for partner in self:
            partner.contact_type = 'student' if partner.is_student else 'guardian'

    def _write_contact_type(self):
        for partner in self:
            partner.is_student = partner.contact_type == 'student'

    @api.model_create_multi
    def create(self, vals_list):
        """ Create method to ensure unique student codes. """
        for vals in vals_list:
            if 'student_code' not in vals or vals['student_code'] == _('New'):
                vals['student_code'] = self.env['ir.sequence'].next_by_code('sequence.student.code') or _('New')
        return super().create(vals_list)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = list(args or [])
        if not name:
            return super().name_search(name=name, args=args, operator=operator, limit=limit)
        domain = ['|', ('name', operator, name), ('student_code', operator, name)]
        if args:
            domain = ['&'] + args + domain
        partners = self.search_fetch(domain, ['display_name'], limit=limit)
        return [(partner.id, partner.display_name) for partner in partners]

    def _get_complete_name(self):
        """ Override to include vendor code in the name. """
        complete_name = super()._get_complete_name()
        if self.student_code and self.is_student:
            complete_name += f" ({self.student_code})"
        return complete_name


