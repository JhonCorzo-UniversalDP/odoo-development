from odoo import fields, models

class LoanApplicationDocument(models.Model):
    _name = 'loan.application.document'
    _description = 'Loan Application Document'

    name = fields.Char(
        string = "Documents"
    )

    application_id = fields.Tags(
        string = "application_id"
    )