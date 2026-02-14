# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _


class Period(models.Model):
    _name = 'algorid.period'
    _description = 'Period/Time Slot'
    _order = 'sequence, start_time'

    name = fields.Char(
        string='Period Name',
        required=True,
        translate=True,
    )
    name_bn = fields.Char(
        string='Period Name (Bangla)',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    start_time = fields.Float(
        string='Start Time',
        required=True,
    )
    end_time = fields.Float(
        string='End Time',
        required=True,
    )
    duration = fields.Float(
        string='Duration (minutes)',
        compute='_compute_duration',
        store=True,
    )
    period_type = fields.Selection([
        ('class', 'Class Period'),
        ('break', 'Break'),
        ('assembly', 'Assembly'),
        ('prayer', 'Prayer'),
        ('lunch', 'Lunch Break'),
    ], string='Period Type', default='class', required=True)
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            record.duration = (record.end_time - record.start_time) * 60

