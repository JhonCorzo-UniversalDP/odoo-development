from odoo import models, fields

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    
    name = fields.Char(string='Application Number', required=True)
    currency_id = field.Many2one(string='Currency',comodel_name='res.currency')
    date_application = field.Date(string='Application Date')
    date_approval = field.Date(string='Approval Date')
    date_rejection = field.Date(string='Rejection Date')
    date_signed = field.Date(string='Signed On')
    down_payment = field.Monetary(string='Downpayment', currency_field='currency_id')
    interest_rate = field.Float(string='Interest Rate (%)', digits=(5, 4))
    loan_amount = field.Monetary(string='Loan Amount', currency_field='currency_id')
    loan_term = field.Integer(string='Loan Term (Months)', required=True, default=36)
    rejection_reason = field.Text(string='Rejection Reason')
    state = field.Selection(string='Status', selection=[('draft', 'Draft'), ('sent', 'Sent'), ('review', 'Credit Check'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('signed', 'Signed'), ('cancel', 'Canceled')], default='draft')
    notes = field.Html(string='Notes')
    
    
    