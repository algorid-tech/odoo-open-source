# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api, _


class MadrasahClass(models.Model):
    _inherit = 'algorid.class'

    @api.depends('section_ids.student_count')
    def _compute_student_count(self):
        for record in self:
            student_count = self.env['algorid.student'].search_count([
                ('class_id', '=', record.id),
                ('state', '=', 'active'),
            ])
            record.student_count = student_count


class Section(models.Model):
    _inherit = 'algorid.section'

    @api.depends()
    def _compute_student_count(self):
        for record in self:
            student_count = self.env['algorid.student'].search_count([
                ('section_id', '=', record.id),
                ('state', '=', 'active'),
            ])
            record.student_count = student_count

