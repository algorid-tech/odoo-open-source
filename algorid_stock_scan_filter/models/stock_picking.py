# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2025 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    scan_status = fields.Selection([
        ('default', 'Default'),
        ('not', 'Not Scanned'),
        ('partial', 'Partially Scanned'),
        ('full', 'Fully Scanned'),
    ], string='Scan Status', compute='_compute_scan_status', store=True, search='_search_scan_status')
    
    @api.depends('state', 'move_ids', 'move_ids.product_uom_qty', 'move_line_ids', 'move_line_ids.qty_done')
    def _compute_scan_status(self):
        """
        Compute the scan status based on scanned quantity vs demand
        - Not Scanned: quantity = 0
        - Partially Scanned: 0 < quantity < demand
        - Fully Scanned: quantity >= demand
        """
        for picking in self:
            if picking.state != 'assigned':
                picking.scan_status = 'default'
                continue

            demand = sum(picking.move_ids.mapped('product_uom_qty'))
            done = sum(picking.move_line_ids.mapped('qty_done'))

            if not demand:
                picking.scan_status = 'default'
            if demand:
                if not done or done == 0:
                    picking.scan_status = 'not'
                elif done == demand:
                    picking.scan_status = 'full'
                elif done < demand:
                    picking.scan_status = 'partial'
                else:
                    picking.scan_status = 'default'
                    
