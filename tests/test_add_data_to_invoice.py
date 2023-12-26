from odoo.tests import TransactionCase
import logging

_logger = logging.getLogger(__name__)


class TestSaleOrderInheritance(TransactionCase):
    """
    Unit tests for _create_invoices method.
    """

    def setUp(self):
        super(TestSaleOrderInheritance, self).setUp()
        self.sale_order = self.env['sale.order'].create({'partner_id': self.env.ref('base.res_partner_1').id})
        self.product_1 = self.env['product.product'].create({
            'name': 'Test Product 1',
            'type': 'consu',
            'invoice_policy': 'order',
            'sale_ok': True,
            'default_code': 'Product Code 1',
        })
        self.product_2 = self.env['product.product'].create({
            'name': 'Test Product 2',
            'type': 'consu',
            'invoice_policy': 'order',
            'sale_ok': True,
            'default_code': 'Product Code 2',
        })
        self.product_3 = self.env['product.product'].create({
            'name': 'Test Product 3',
            'type': 'consu',
            'invoice_policy': 'order',
            'sale_ok': True,
            'default_code': 'Product Code 3',
        })
        self.product_4 = self.env['product.product'].create({
            'name': 'Test Product 4',
            'type': 'consu',
            'invoice_policy': 'order',
            'sale_ok': True,
            'default_code': 'Product Code 3',
        })

        self.prekes_zenklas_1 = self.env['prekes.zenklas'].create({'name': 'Zenklas 1'})
        self.prekes_zenklas_2 = self.env['prekes.zenklas'].create({'name': 'Zenklas 2'})
        self.prekes_zenklas_3 = self.env['prekes.zenklas'].create({'name': 'Zenklas 3'})
        self.prekes_zenklas_4 = self.env['prekes.zenklas'].create({'name': 'Zenklas 4'})
        self.prekes_zenklas_5 = self.env['prekes.zenklas'].create({'name': 'Zenklas 5'})
        self.prekes_zenklas_6 = self.env['prekes.zenklas'].create({'name': 'Zenklas 6'})
        self.prekes_zenklas_7 = self.env['prekes.zenklas'].create({'name': 'Zenklas 7'})
        self.prekes_zenklas_8 = self.env['prekes.zenklas'].create({'name': 'Zenklas 8'})

    def test_create_invoices_1(self):
        """
        Test _create_invoices.
        Creating Invoice with one Invoice Line, from Sale Order with one Sale Order Line, with no prekes_zenklas
        assigned.
        """
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            # No prekes_zenklas added to this Sale Order Line
        })

        self.sale_order.state = 'sale'

        invoices = self.sale_order._create_invoices()

        self.assertEqual(len(invoices), 1, 'Expected one invoice to be created')
        self.assertEqual(len(invoices.invoice_line_ids), 1, 'Expected one invoice line')
        self.assertEqual(len(invoices.invoice_line_ids.prekes_zenklai_ids), 0,
                         'Expected no prekes_zenklas to be copied to Invoice Line prekes_zenklai_ids from Sale Order \
                         Line')

        self.assertEqual(invoices.narration, False,
                         'Expected narration value to be "False"')

        _logger.info("Test test_create_invoices_1 passed.")

    def test_create_invoices_2(self):
        """
        Test _create_invoices.
        Creating Invoice with 1 Invoice Line, from Sale Order with 1 Sale Order Line, with 1 prekes_zenklas
        assigned.
        """
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [(6, 0, [self.prekes_zenklas_1.id])]
        })

        self.sale_order.state = 'sale'

        invoices = self.sale_order._create_invoices()

        self.assertEqual(len(invoices), 1, 'Expected one invoice to be created')
        self.assertEqual(len(invoices.invoice_line_ids), 1, 'Expected one invoice line')
        self.assertEqual(len(invoices.invoice_line_ids.prekes_zenklai_ids), 1,
                         'Expected one prekes_zenklas to be copied to Invoice\'s prekes_zenklai_ids from Sale Order')
        self.assertEqual(invoices.invoice_line_ids.prekes_zenklai_ids[0].name, 'Zenklas 1',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 1"')
        self.assertEqual(invoices.narration, '<p>Product Code 1 - (Zenklas 1)</p>',
                         'Expected narration value added to Invoice is "<p>Product Code 1 - (Zenklas 1)</p>"')

        _logger.info("Test test_create_invoices_2 passed.")

    def test_create_invoices_3(self):
        """
        Test _create_invoices.
        Creating Invoice with 2 Invoice Lines, from Sale Order with 2 Sale Order Lines. 2 different products assigned.
        prekes_zenklas assigned just to one Invoice Line.
        """
        sale_order_line_1 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            # prekes_zenklas is not assigned to prekes_zenklai_ids for this Sale Order Line
        })
        sale_order_line_2 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_2.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [(6, 0, [self.prekes_zenklas_2.id])]
        })

        self.sale_order.state = 'sale'

        invoices = self.sale_order._create_invoices()

        self.assertEqual(len(invoices), 1, 'Expected one invoice to be created')
        self.assertEqual(len(invoices.invoice_line_ids), 2, 'Expected 2 Invoice Lines')
        self.assertEqual(len(invoices.invoice_line_ids.prekes_zenklai_ids), 1,
                         'Expected one prekes_zenklas to be copied to Invoice Line prekes_zenklai_ids from Sale Order')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[0].name, 'Zenklas 2',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 2"')
        self.assertEqual(invoices.narration, '<p>Product Code 2 - (Zenklas 2)</p>',
                         'Expected narration value added to Invoice is "<p>Product Code 2 - (Zenklas 2)</p>"')

        _logger.info("Test test_create_invoices_3 passed.")

    def test_create_invoices_4(self):
        """
        Test _create_invoices.
        Creating Invoice with 2 Invoice Lines, from Sale Order with 2 Sale Order Lines. 2 different products assigned.
        1 prekes_zenklas assigned to each Invoice Line.
        """
        sale_order_line_1 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [(6, 0, [self.prekes_zenklas_1.id])]
        })
        sale_order_line_2 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_2.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [(6, 0, [self.prekes_zenklas_2.id])]
        })

        self.sale_order.state = 'sale'

        invoices = self.sale_order._create_invoices()

        self.assertEqual(len(invoices), 1, 'Expected one invoice to be created')
        self.assertEqual(len(invoices.invoice_line_ids), 2, 'Expected 2 Invoice Lines')

        self.assertEqual(len(invoices.invoice_line_ids[0].prekes_zenklai_ids), 1,
                         'Expected 1 prekes_zenklas to be copied to Invoice Line #1 prekes_zenklai_ids from Sale Order')
        self.assertEqual(len(invoices.invoice_line_ids[1].prekes_zenklai_ids), 1,
                         'Expected 1 prekes_zenklas to be copied to Invoice Line #2 prekes_zenklai_ids from Sale Order')

        self.assertEqual(invoices.invoice_line_ids[0].prekes_zenklai_ids[0].name, 'Zenklas 1',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 1"')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[0].name, 'Zenklas 2',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 2"')

        self.assertEqual(str(invoices.narration),
                         '<p>Product Code 1 - (Zenklas 1)<br><br>Product Code 2 - (Zenklas 2)</p>',
                         'Expected narration value added to Invoice is "<p>Product Code 1 - (Zenklas 1)<br><br>Product Code 2 - (Zenklas 2)</p>"')

        _logger.info("Test test_create_invoices_4 passed.")

    def test_create_invoices_5(self):
        """
        Test _create_invoices.
        Creating Invoice with 3 Invoice Lines, from Sale Order with 3 Sale Order Lines. 2 different products assigned.
        Invoice Line #1 and Invoice Line #2 contain the same product, but prekes_zenklai_ids contain different brand
        names. Invoice Line #2, on prekes_zenklai_ids field contain 8 different brand names.
        """
        sale_order_line_1 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [
                (6, 0, [self.prekes_zenklas_1.id, self.prekes_zenklas_2.id, self.prekes_zenklas_3.id])]
        })
        sale_order_line_2 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_2.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [(6, 0,
                                    [
                                        self.prekes_zenklas_1.id,
                                        self.prekes_zenklas_2.id,
                                        self.prekes_zenklas_3.id,
                                        self.prekes_zenklas_4.id,
                                        self.prekes_zenklas_5.id,
                                        self.prekes_zenklas_6.id,
                                        self.prekes_zenklas_7.id,
                                        self.prekes_zenklas_8.id,
                                    ])]
        })
        sale_order_line_3 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [(6, 0, [
                self.prekes_zenklas_4.id, self.prekes_zenklas_5.id, self.prekes_zenklas_6.id
            ])]
        })

        self.sale_order.state = 'sale'

        invoices = self.sale_order._create_invoices()

        self.assertEqual(len(invoices), 1, 'Expected one invoice to be created')
        self.assertEqual(len(invoices.invoice_line_ids), 3, 'Expected 3 Invoice Lines')

        self.assertEqual(len(invoices.invoice_line_ids[0].prekes_zenklai_ids), 3,
                         'Expected 3 prekes_zenklas to be copied to Invoice Line #1 prekes_zenklai_ids from Sale Order')
        self.assertEqual(len(invoices.invoice_line_ids[1].prekes_zenklai_ids), 8,
                         'Expected 8 prekes_zenklas to be copied to Invoice Line #2 prekes_zenklai_ids from Sale Order')
        self.assertEqual(len(invoices.invoice_line_ids[2].prekes_zenklai_ids), 3,
                         'Expected 3 prekes_zenklas to be copied to Invoice Line #3 prekes_zenklai_ids from Sale Order')

        # 3 different prekes_zenklas added to Invoice line #1.
        self.assertEqual(invoices.invoice_line_ids[0].prekes_zenklai_ids[0].name, 'Zenklas 1',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 1"')
        self.assertEqual(invoices.invoice_line_ids[0].prekes_zenklai_ids[1].name, 'Zenklas 2',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 2"')
        self.assertEqual(invoices.invoice_line_ids[0].prekes_zenklai_ids[2].name, 'Zenklas 3',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 3"')

        # 8 different prekes_zenklas added to Invoice line #2.
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[0].name, 'Zenklas 1',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 1"')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[1].name, 'Zenklas 2',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 2"')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[2].name, 'Zenklas 3',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 3"')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[3].name, 'Zenklas 4',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 4"')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[4].name, 'Zenklas 5',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 5"')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[5].name, 'Zenklas 6',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 6"')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[6].name, 'Zenklas 7',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 7"')
        self.assertEqual(invoices.invoice_line_ids[1].prekes_zenklai_ids[7].name, 'Zenklas 8',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 8"')

        # 3 different prekes_zenklas added to Invoice line #3.
        self.assertEqual(invoices.invoice_line_ids[2].prekes_zenklai_ids[0].name, 'Zenklas 4',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 4"')
        self.assertEqual(invoices.invoice_line_ids[2].prekes_zenklai_ids[1].name, 'Zenklas 5',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 5"')
        self.assertEqual(invoices.invoice_line_ids[2].prekes_zenklai_ids[2].name, 'Zenklas 6',
                         'Expected prekes_zenklas on Invoice line is "Zenklas 6"')

        self.assertEqual(str(invoices.narration),
                         '<p>Product Code 1 - (Zenklas 1, Zenklas 2, Zenklas 3, Zenklas 4, Zenklas 5, Zenklas 6)<br><br>Product Code 2 - (Zenklas 1, Zenklas 2, Zenklas 3, Zenklas 4, Zenklas 5, Zenklas 6, Zenklas 7, Zenklas 8)</p>',
                         'Expected narration value added to Invoice is "<p>Product Code 1 - (Zenklas 1, Zenklas 2, Zenklas 3, Zenklas 4, Zenklas 5, Zenklas 6)<br><br>Product Code 2 - (Zenklas 1, Zenklas 2, Zenklas 3, Zenklas 4, Zenklas 5, Zenklas 6, Zenklas 7, Zenklas 8)</p>"')

        _logger.info("Test test_create_invoices_5 passed.")

    def test_create_invoices_6(self):
        """
        Test _create_invoices.

        Creating 6 Sale Order Lines for Sale Order:
        Sale Order Line #1. Added: Product 1, Zenklas 1, Zenklas 2, Zenklas 3
        Sale Order Line #2. Added: Product 2,
        Sale Order Line #3. Added: Product 3, Zenklas 1, Zenklas 4, Zenklas 5
        Sale Order Line #4. Added: Product 4, Zenklas 6, Zenklas 8
        Sale Order Line #5. Added: Product 1, Zenklas 1, Zenklas 2
        Sale Order Line #6. Added: Product 2, Zenklas 4, Zenklas 6, Zenklas 7

        Expected 'narration' field on Invoice:
        "
        Product Code 1 - (Zenklas 1, Zenklas 2, Zenklas 3)

        Product Code 3 - (Zenklas 1, Zenklas 4, Zenklas 5)

        Product Code 4 - (Zenklas 6, Zenklas 8)

        Product Code 2 - (Zenklas 4, Zenklas 6, Zenklas 7)
        "
        """

        sale_order_line_1 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [
                (6, 0, [self.prekes_zenklas_1.id, self.prekes_zenklas_2.id, self.prekes_zenklas_3.id])]
        })

        sale_order_line_2 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_2.id,
            'product_uom_qty': 1,
            'price_unit': 100,
        })

        sale_order_line_3 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_3.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [
                (6, 0, [self.prekes_zenklas_1.id, self.prekes_zenklas_4.id, self.prekes_zenklas_5.id])]
        })

        sale_order_line_4 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_4.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [
                (6, 0, [self.prekes_zenklas_6.id, self.prekes_zenklas_8.id])]
        })

        sale_order_line_5 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [
                (6, 0, [self.prekes_zenklas_1.id, self.prekes_zenklas_2.id])]
        })

        sale_order_line_6 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_2.id,
            'product_uom_qty': 1,
            'price_unit': 100,
            'prekes_zenklai_ids': [
                (6, 0, [self.prekes_zenklas_4.id, self.prekes_zenklas_6.id, self.prekes_zenklas_7.id])]
        })


        self.sale_order.state = 'sale'

        invoices = self.sale_order._create_invoices()

        self.assertEqual(len(invoices), 1, 'Expected one invoice to be created')
        self.assertEqual(len(invoices.invoice_line_ids), 6, 'Expected 6 Invoice Lines')

        self.assertEqual(str(invoices.narration),
                         '<p>Product Code 1 - (Zenklas 1, Zenklas 2, Zenklas 3)\
                         <br><br>\
                         Product Code 3 - (Zenklas 1, Zenklas 4, Zenklas 5)\
                         <br><br>\
                         Product Code 4 - (Zenklas 6, Zenklas 8)\
                         <br><br>\
                         Product Code 2 - (Zenklas 4, Zenklas 6, Zenklas 7)</p>',
                         'Expected narration value added to Invoice is "<p>Product Code 1 - (Zenklas 1, Zenklas 2, Zenklas 3)\
                         <br><br>\
                         Product Code 3 - (Zenklas 1, Zenklas 4, Zenklas 5)\
                         <br><br>\
                         Product Code 4 - (Zenklas 6, Zenklas 8)\
                         <br><br>\
                         Product Code 2 - (Zenklas 4, Zenklas 6, Zenklas 7)</p>"')

        _logger.info("Test test_create_invoices_6 passed.")

# Note: Running tests
# ./odoo-bin -c /home/marty1544/Odoo/16.0/.odoorc -u prekes_zenklai --test-enable
