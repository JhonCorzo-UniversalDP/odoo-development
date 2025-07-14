from odoo import models, fields, api

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    
    name = fields.Char(
        string='Name', 
        required=True
    )

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Related Sale Order' 
    )

    # ? Extraer currency_id, desde la orden de venta
    currency_id = fields.Many2one(
        comodel_name = "res.currency",
        related = "sale_order_id.currency_id",
        string = 'Currency',
    )
    # currency_id = fields.Many2one(
    #     comodel_name='res.currency', 
    #     string='Currency', 
    #     default=lambda self:self.env.company.currency_id.id
    # )
    
    date_application = fields.Date(
        string='Application Date', 
        # readonly=True, 
        copy=False
    )
    
    date_approval = fields.Date(
        string='Approval Date',
        readonly=True, 
        copy=False
    )
    
    date_rejection = fields.Date(
        string='Rejection Date', 
        readonly=True, 
        copy=False
    )
    
    date_signed = fields.Date(
        string='Signed On', 
        readonly=True, 
        copy=False
    )
    
    down_payment = fields.Monetary(
        string='Downpayment', 
        currency_field='currency_id', 
        required=True
    )
    
    interest_rate = fields.Float(
        string='Interest Rate (%)', 
        digits=(5, 4), 
        required=True
    )

    # ? Extraer el total de la venta, desde la orden de venta 
    sale_order_total = fields.Monetary(
        related = 'sale_order_id.amount_total',
        string = 'Sale Order Total'
        # currency_field = 'currency_id'
    )


    # ? Calcular restando el anticipo total del pedidio (down_payment) de la venta (sale_order_total)
    loan_amount = fields.Monetary(
        compute = '_calculate_loan_amount',
        string = 'Loan Amount'
    )

    @api.depends('sale_order_total', 'down_payment')
    def _calculate_loan_amount(self):
        for record in self:
            record.loan_amount = record.sale_order_total - record.down_payment
    # loan_amount = fields.Monetary(
    #     string='Loan Amount', 
    #     currency_field='currency_id', 
    #     required=True
    # )
    
    loan_term = fields.Integer(
        string='Loan Term (Months)', 
        required=True, 
        default=36
    )
    
    rejection_reason = fields.Text(
        string='Rejection Reason', 
        copy=False
    )

    state = fields.Selection(
        string='Status', 
        selection=[
            ('draft', 'Draft'), 
            ('sent', 'Sent'), 
            ('review', 'Credit Check'), 
            ('approved', 'Approved'), 
            ('rejected', 'Rejected'), 
            ('signed', 'Signed'), 
            ('cancel', 'Canceled')
        ], 
        default='draft',
        copy=False
    )

    notes = fields.Html(
        string='Notes',
        copy=False
    )

    # ? Extraer partner_id, desde la orden de venta
    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        related = "sale_order_id.partner_id",
        string = "Customer"
    )
    # partner_id = fields.Many2one(
    #     comodel_name='res.partner',
    #     string='Customer'
    # )

    # ? Extraer user_id, desde la orden de venta
    user_id = fields.Many2one(
        comodel_name = 'res.users',
        related = 'sale_order_id.user_id',
        string = 'Salesperson'
    )
    # user_id = fields.Many2one(
    #     comodel_name='res.users',
    #     string='Salesperson'
    # )

    product_template_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )

    documentation_ids = fields.One2many(
        comodel_name = 'loan.application.document',
        inverse_name = 'application_id',
        string = 'Documentation'
    )
    
    