from odoo import models, fields

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    
    name = fields.Char(
        string='Name', 
        required=True
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency', 
        string='Currency', 
        default=lambda self:self.env.company.currency_id.id
    )
    
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
    
    loan_amount = fields.Monetary(
        string='Loan Amount', 
        currency_field='currency_id', 
        required=True
    )
    
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
            ('cancel', 'Canceled')\
        ], 
        default='draft',
        copy=False
    )

    notes = fields.Html(
        string='Notes',
        copy=False
    )
    
    
    