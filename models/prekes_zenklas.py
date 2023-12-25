# -*- coding: utf-8 -*-
from odoo import models, fields


class PrekesZenklas(models.Model):
    """
    Created new model.
    """
    _name = 'prekes.zenklas'
    _description = 'Prekes Zenklas'

    name = fields.Char(string='Name')
