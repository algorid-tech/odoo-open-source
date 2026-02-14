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
from dateutil.relativedelta import relativedelta


class Student(models.Model):
    _name = 'algorid.student'
    _description = 'Student'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _order = 'name'
    _rec_name = 'display_name'

    # Basic Information
    name = fields.Char(
        string='Student Name',
        required=True,
        tracking=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Student Name (Bangla)',
        tracking=True,
    )
    student_id = fields.Char(
        string='Student ID',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True,
    )
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
    )

    # Personal Information
    date_of_birth = fields.Date(
        string='Date of Birth',
        tracking=True,
    )
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', required=True, default='male', tracking=True)
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string='Blood Group')
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('other', 'Other'),
    ], string='Religion', default='islam')
    nationality = fields.Char(
        string='Nationality',
        default='Bangladeshi',
    )
    birth_certificate_no = fields.Char(
        string='Birth Certificate No',
    )
    national_id = fields.Char(
        string='National ID',
    )

    # Contact Information
    phone = fields.Char(
        string='Phone',
    )
    mobile = fields.Char(
        string='Mobile',
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

    # Permanent Address
    permanent_street = fields.Char(
        string='Permanent Street',
    )
    permanent_street2 = fields.Char(
        string='Permanent Street 2',
    )
    permanent_city = fields.Char(
        string='Permanent City',
    )
    permanent_state_id = fields.Many2one(
        'res.country.state',
        string='Permanent State',
    )
    permanent_zip = fields.Char(
        string='Permanent ZIP',
    )
    permanent_country_id = fields.Many2one(
        'res.country',
        string='Permanent Country',
        default=lambda self: self.env.ref('base.bd', raise_if_not_found=False),
    )
    same_as_present = fields.Boolean(
        string='Same as Present Address',
        default=True,
    )

    # Academic Information
    academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Academic Year',
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
        tracking=True,
        domain="[('class_id', '=', class_id)]",
    )
    roll_no = fields.Integer(
        string='Roll Number',
        tracking=True,
    )
    admission_date = fields.Date(
        string='Admission Date',
        default=fields.Date.today,
        tracking=True,
    )
    admission_class_id = fields.Many2one(
        'algorid.class',
        string='Admission Class',
    )
    previous_school = fields.Char(
        string='Previous School',
    )

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('left', 'Left'),
        ('suspended', 'Suspended'),
    ], string='Status', default='draft', required=True, tracking=True)
    leaving_date = fields.Date(
        string='Leaving Date',
    )
    leaving_reason = fields.Text(
        string='Leaving Reason',
    )

    # Guardian Information
    guardian_id = fields.Many2one(
        'algorid.guardian',
        string='Primary Guardian',
        tracking=True,
    )
    guardian_ids = fields.Many2many(
        'algorid.guardian',
        'student_guardian_rel',
        'student_id',
        'guardian_id',
        string='Guardians',
    )
    father_name = fields.Char(
        string="Father's Name",
    )
    father_name_bn = fields.Char(
        string="Father's Name (Bangla)",
    )
    father_phone = fields.Char(
        string="Father's Phone",
    )
    father_occupation = fields.Char(
        string="Father's Occupation",
    )
    mother_name = fields.Char(
        string="Mother's Name",
    )
    mother_name_bn = fields.Char(
        string="Mother's Name (Bangla)",
    )
    mother_phone = fields.Char(
        string="Mother's Phone",
    )
    mother_occupation = fields.Char(
        string="Mother's Occupation",
    )

    # Tags
    tag_ids = fields.Many2many(
        'algorid.student.tag',
        'student_tag_rel',
        'student_id',
        'tag_id',
        string='Tags',
    )

    # Documents
    document_ids = fields.One2many(
        'algorid.student.document',
        'student_id',
        string='Documents',
    )
    document_count = fields.Integer(
        string='Document Count',
        compute='_compute_document_count',
    )

    # Medical Information
    medical_info = fields.Text(
        string='Medical Information',
    )
    allergies = fields.Text(
        string='Allergies',
    )
    emergency_contact = fields.Char(
        string='Emergency Contact',
    )
    emergency_phone = fields.Char(
        string='Emergency Phone',
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

    _sql_constraints = [
        ('student_id_unique', 'unique(student_id, company_id)',
         'Student ID must be unique!'),
    ]

    @api.depends('name', 'student_id')
    def _compute_display_name(self):
        for record in self:
            if record.student_id and record.student_id != _('New'):
                record.display_name = f"[{record.student_id}] {record.name}"
            else:
                record.display_name = record.name

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                record.age = relativedelta(today, record.date_of_birth).years
            else:
                record.age = 0

    @api.depends('document_ids')
    def _compute_document_count(self):
        for record in self:
            record.document_count = len(record.document_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('student_id', _('New')) == _('New'):
                vals['student_id'] = self.env['ir.sequence'].next_by_code(
                    'algorid.student'
                ) or _('New')
        return super().create(vals_list)

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.section_id = False
        if self.class_id:
            return {
                'domain': {
                    'section_id': [('class_id', '=', self.class_id.id)]
                }
            }

    @api.onchange('same_as_present')
    def _onchange_same_as_present(self):
        if self.same_as_present:
            self.permanent_street = self.street
            self.permanent_street2 = self.street2
            self.permanent_city = self.city
            self.permanent_state_id = self.state_id
            self.permanent_zip = self.zip
            self.permanent_country_id = self.country_id

    def action_activate(self):
        """Activate the student."""
        self.write({'state': 'active'})

    def action_graduate(self):
        """Mark student as graduated."""
        self.write({
            'state': 'graduated',
            'leaving_date': fields.Date.today(),
        })

    def action_leave(self):
        """Mark student as left."""
        self.write({
            'state': 'left',
            'leaving_date': fields.Date.today(),
        })

    def action_suspend(self):
        """Suspend the student."""
        self.write({'state': 'suspended'})

    def action_draft(self):
        """Reset to draft."""
        self.write({'state': 'draft'})

    def action_view_documents(self):
        """View student documents."""
        self.ensure_one()
        return {
            'name': _('Documents'),
            'type': 'ir.actions.act_window',
            'res_model': 'algorid.student.document',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_create_portal_user(self):
        """Create portal user for the student."""
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

