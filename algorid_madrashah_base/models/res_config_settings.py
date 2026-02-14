# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################
from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    madrashah_name = fields.Char(
        string='Madrashah Name',
        config_parameter='algorid_madrashah.name',
    )
    madrashah_name_bn = fields.Char(
        string='Madrashah Name (Bangla)',
        config_parameter='algorid_madrashah.name_bn',
    )
    late_fee_grace_days = fields.Integer(
        string='Late Fee Grace Days',
        config_parameter='algorid_madrashah.late_fee_grace_days',
        default=10,
    )
    late_fee_percentage = fields.Float(
        string='Late Fee Percentage',
        config_parameter='algorid_madrashah.late_fee_percentage',
        default=5.0,
    )
    current_academic_year_id = fields.Many2one(
        'algorid.academic.year',
        string='Current Academic Year',
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        academic_year_id = ICPSudo.get_param('algorid_madrashah.current_academic_year_id')
        res.update(
            current_academic_year_id=int(academic_year_id) if academic_year_id else False,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('algorid_madrashah.current_academic_year_id', self.current_academic_year_id.id if self.current_academic_year_id else False)

