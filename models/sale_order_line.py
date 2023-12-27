# -*- coding: utf-8 -*-
from odoo import models, fields


class PrekesZenklasOnSaleOrderLine(models.Model):
    """
    Inheriting Sale Order Line model and adding new Many2many field to it.
    Created 'sale_order_line_prekes_zenklas_rel' relation table.
    """
    _inherit = 'sale.order.line'

    prekes_zenklai_ids = fields.Many2many(
        'prekes.zenklas', 'sale_order_line_prekes_zenklas_rel', 'sale_order_line_id', 'prekes_zenklas_id',
        string='Prekes Zenklai'
    )
