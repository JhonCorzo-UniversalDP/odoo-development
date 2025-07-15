from odoo import fields,models

class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = "Loan Application Tag"
    _order = "name"

    name = fields.Char(
        string="Tag",
        required=True
    )

    color = fields.Integer(
        string = "Color", 
        required = True
    )

    _sql_constraints = [
        ("name_is_unique", "UNIQUE(name)", "The tag name must be unique")
    ]
