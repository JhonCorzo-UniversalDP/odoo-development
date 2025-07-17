import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'
    _order = 'date_application desc, name'
    _logger = logging.getLogger(__name__)
    
    #region Loan Application fields
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
        string = 'Sale Order Total',
        currency_field = 'currency_id'
    )


    # ? Calcular restando el anticipo total del pedidio (down_payment) de la venta (sale_order_total)
    loan_amount = fields.Monetary(
        compute = '_calculate_loan_amount',
        string = 'Loan Amount',
        currency_field='currency_id'

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
            ('signed', 'Signed'), 
            ('approved', 'Approved'), 
            ('cancel', 'Canceled'),
            ('rejected', 'Rejected')
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
        related = 'sale_order_id.order_line.product_id',
        string='Product'
    )

    documentation_ids = fields.One2many(
        comodel_name = 'loan.application.document',
        inverse_name = 'application_id',
        string = 'Documentation'
    )

    tags = fields.Many2many(
        comodel_name = 'loan.application.tag',
        string = 'Tags'
    )
    #endregion

    #region Validations
    _sql_constraints = [
        ('down_payment_is_positive', 'CHECK(down_payment >= 0)', "The down payment can't be zero nor negative")
    ]

    @api.constrains('down_payment', 'sale_order_total')
    def _check_down_payment(self):
        for record in self:
            if(record.down_payment >= record.sale_order_total):
                raise ValidationError("The down payment can't be equal or greater than the total amount")

    @api.constrains('sale_order_id')
    def _check_saler_order(self):
        self.ensure_one()
        is_valid, message = self.sale_order_id.can_apply_loan()

        if(not is_valid):
            raise ValidationError(message)

    

    #endregion

    #region Methods

    @api.depends('partner_id', 'product_template_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f'{record.partner_id.name} {"" if not record.product_template_id else "-" } {"" if not record.product_template_id else record.product_template_id.name }'


    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        # Actualizar is_financed en sale.order
        for record in records:
            if record.sale_order_id:
                record.sale_order_id.write({'is_financed': True})

        self._create_documents_foreach_type(records)

        return records

    def _create_documents_foreach_type(self, records):
        document_types = self.env["loan.application.document.type"].search([('active', '=', True)])
        record_documents = []

        for record in records:
            for doc_type in document_types:
                record_documents.append(
                    {
                        "name": f"{record.partner_id.name} - {doc_type.name}",
                        "application_id": record.id,
                        "type_id": doc_type.id
                    }
                )
        
        if record_documents:
            self.env['loan.application.document'].create(record_documents)
    #endregion

    #region Button Actions
    def sent_for_approval(self):
        for record in self:
            # self._logger.info(f"Documentos {record.documentation_ids}")
            has_pending_docs = any(doc.state != 'approved' for doc in record.documentation_ids)
            
            if has_pending_docs:
                raise ValidationError("The Loan Application has rejected or new documents")
            else:
                self.write({'state': 'sent'})

    def approve_application(self):
        self.write({'state': 'approved'})
        self.write({'date_approval': datetime.datetime.now()})

    def reject_application(self):
        self.write({'state': 'rejected'})

    @api.constrains('state', 'rejection_reason')
    def _check_empty_rejection_reason(self):
        for record in self:
            if record.state == 'rejected' and not record.rejection_reason:
                raise ValidationError("Please add the rejection details")
    
    #endregion
    
    