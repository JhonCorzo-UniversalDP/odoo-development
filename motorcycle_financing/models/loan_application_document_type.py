from odoo import fields, models

class LoanApplicationDocumentType(models.Model):
    _name = "loan.application.document.type"
    _description = "Loan Application Document Type"

    name = fields.Char(
        string = "Documents",
        copy = False,
        required = True
    )

    active = fields.Boolean(
        string = "Active",
        default = True
    )