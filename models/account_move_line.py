# -*- coding: utf-8 -*-
from odoo import models, fields


class PrekesZenklasOnInvoiceLine(models.Model):
    """
    Inheriting Invoice Line model and adding new Many2many field to it.
    """
    _inherit = 'account.move.line'

    prekes_zenklai_ids = fields.Many2many(
        'prekes.zenklas', 'invoice_line_prekes_zenklas_rel', 'invoice_line_id', 'prekes_zenklas_id',
        string='Prekes Zenklai'
    )
