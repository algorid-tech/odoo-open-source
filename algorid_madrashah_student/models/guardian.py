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


class Guardian(models.Model):
    _name = 'algorid.guardian'
    _description = 'Student Guardian'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _order = 'name'

    name = fields.Char(
        string='Guardian Name',
        required=True,
        tracking=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Guardian Name (Bangla)',
    )
    relation = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
        ('grandfather', 'Grandfather'),
        ('grandmother', 'Grandmother'),
        ('guardian', 'Legal Guardian'),
        ('other', 'Other'),
    ], string='Relation', required=True, default='father', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    date_of_birth = fields.Date(
        string='Date of Birth',
    )
    national_id = fields.Char(
        string='National ID',
    )
    occupation = fields.Char(
        string='Occupation',
    )
    designation = fields.Char(
        string='Designation',
    )
    organization = fields.Char(
        string='Organization',
    )
    monthly_income = fields.Float(
        string='Monthly Income',
    )

    # Contact Information
    phone = fields.Char(
        string='Phone',
    )
    mobile = fields.Char(
        string='Mobile',
        required=True,
    )
    email = fields.Char(
        string='Email',
    )

    # Address
    street = fields.Char(
        string='Street',
    )
    street2 = fields.Char(
        string='Street 2',
    )
    city = fields.Char(
        string='City',
    )
    state_id = fields.Many2one(
        'res.country.state',
        string='State',
    )
    zip = fields.Char(
        string='ZIP',
    )
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        default=lambda self: self.env.ref('base.bd', raise_if_not_found=False),
    )

    # Related Students
    student_ids = fields.Many2many(
        'algorid.student',
        'student_guardian_rel',
        'guardian_id',
        'student_id',
        string='Students',
    )
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_student_count',
    )

    # Other
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Portal User',
        copy=False,
    )
    notes = fields.Text(
        string='Notes',
    )
    is_emergency_contact = fields.Boolean(
        string='Emergency Contact',
        default=False,
    )

    @api.depends('student_ids')
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)

    @api.onchange('relation')
    def _onchange_relation(self):
        if self.relation in ['father', 'brother', 'uncle', 'grandfather']:
            self.gender = 'male'
        elif self.relation in ['mother', 'sister', 'aunt', 'grandmother']:
            self.gender = 'female'

    def action_view_students(self):
        """View guardian's students."""
        self.ensure_one()
        return {
            'name': _('Students'),
            'type': 'ir.actions.act_window',
            'res_model': 'algorid.student',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.student_ids.ids)],
        }

    def action_create_portal_user(self):
        """Create portal user for the guardian."""
        self.ensure_one()
        if self.user_id:
            raise ValidationError(_('Portal user already exists!'))
        if not self.email:
            raise ValidationError(_('Email is required to create portal user!'))

        # Create user with portal access
        user = self.env['res.users'].sudo().create({
            'name': self.name,
            'login': self.email,
            'email': self.email,
            'active': True,
        })

        # Add user to portal group only
        portal_group = self.env.ref('base.group_portal')
        internal_group = self.env.ref('base.group_user')
        internal_group.sudo().write({'user_ids': [(3, user.id)]})
        portal_group.sudo().write({'user_ids': [(4, user.id)]})

        self.user_id = user.id
        user.action_reset_password()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Portal user created successfully!'),
                'type': 'success',
            }
        }

