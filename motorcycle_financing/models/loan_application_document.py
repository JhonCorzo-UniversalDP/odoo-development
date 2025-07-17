from odoo import fields, models, api
from odoo.exceptions import ValidationError

class LoanApplicationDocument(models.Model):
    _name = 'loan.application.document'
    _description = 'Loan Application Document'
    _order = "sequence asc"

    sequence = fields.Integer(default=10)

    name = fields.Char(
        string = "Documents",
        copy = False,
    )

    application_id = fields.Many2one(
        comodel_name = 'loan.application',
        string = "Application",
        required = True
    )

    attachment = fields.Binary(
        attachment = True,
        string = "Attachment",
        copy = False,
    )

    type_id = fields.Many2one(
        comodel_name = "loan.application.document.type",
        string = "Type",
        required = True
    )

    state = fields.Selection(
        string = "State",
        selection = [
            ('new', 'New'),
            ('approved','Approved'),
            ('rejected','Rejected')
        ],
        default = 'new',
        copy = False
    )

    def action_approve(self):
        # Actualizar state
        self.write({'state': 'approved'})

    def action_reject(self):
        # Actualizar state
        self.write({'state': 'rejected'})

    @api.onchange('name','application_id','attachment', 'type_id')
    def _onchange_required_fields(self):
        self.state = "new"