# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2025 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_import_packaging_excel(self):
        """Open import wizard filtered for this product"""
        self.ensure_one()
        
        return {
            'name': f'Import Packaging - {self.display_name}',
            'type': 'ir.actions.act_window',
            'res_model': 'product.packaging.import.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_filter_product_id': self.id,
            }
        }
