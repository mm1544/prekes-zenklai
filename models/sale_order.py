# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False, date=None):
        """
        Inheriting Sale Order model and overwriting _create_invoices method.
        For each Invoice Line of created Invoice, access related Sale Order Line, collect all assigned Prekes Zenklas
        and copy to related Invoice Line's prekes_zenklai_ids field.
        Format html code and assign to 'narration' field.
        """
        res = super(SaleOrder, self)._create_invoices()
        products_with_brands = {}
        if not res:
            return res

        for invoice in res:
            try:
                for inv_line in invoice.invoice_line_ids:
                    so_prekes_zenklai = []

                    # Collect prekes_zenklai_ids from related sale order lines
                    if inv_line.sale_line_ids:
                        so_prekes_zenklai += inv_line.sale_line_ids.prekes_zenklai_ids.ids

                    # Update prekes_zenklai_ids field in the current invoice line
                    if so_prekes_zenklai:
                        inv_line.write({'prekes_zenklai_ids': [(6, 0, so_prekes_zenklai)]})

                        # Update products_with_brands dictionary
                        product_code = inv_line.product_id.default_code
                        if product_code:
                            products_with_brands.setdefault(product_code, []).extend(so_prekes_zenklai)

                info_text_html = ''

                # Format info_text_html with product codes and corresponding brand names
                for p_code, brand_name_id_list in products_with_brands.items():
                    brand_names = list(set(self.env['prekes.zenklas'].browse(brand_name_id_list).mapped('name')))
                    if brand_names:
                        brand_names.sort()

                    brand_name_text = ', '.join(brand_names)
                    info_text_html += '{} - ({})<br><br>'.format(p_code, brand_name_text)

                # Update narration field in the current invoice with formatted info_text_html
                if info_text_html:
                    info_text_html = info_text_html[:-8]
                    invoice.write({'narration': info_text_html})

            except Exception as e:
                _logger.error("An error occurred: %s", str(e))

        return res
