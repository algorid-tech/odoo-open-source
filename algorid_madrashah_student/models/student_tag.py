# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _


class StudentTag(models.Model):
    _name = 'algorid.student.tag'
    _description = 'Student Tag'
    _order = 'name'

    name = fields.Char(
        string='Tag Name',
        required=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Tag Name (Bangla)',
    )
    color = fields.Integer(
        string='Color',
        default=0,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    description = fields.Text(
        string='Description',
        translate=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        ('name_unique', 'unique(name, company_id)',
         'Tag name must be unique!'),
    ]

