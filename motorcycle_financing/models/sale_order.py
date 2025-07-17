from odoo import fields, models, api
import logging
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = "sale.order"

    loan_application_id = fields.One2many(
        comodel_name="loan.application",
        inverse_name="sale_order_id",
        string = "Loan Application"
    )

    is_financed = fields.Boolean(
        string="Financed",
        default=False
    )

    state = fields.Selection(
        selection_add=[
            ('loan_pending','Loan Pending')
        ]
    )

    @api.constrains("order_line")
    def apply_loan(self):
        self.ensure_one()

        # for line in self.order_line:
        #     self._logger.info(f"Line {line}")

        if(len(self.order_line) > 1):
            raise ValidationError("The order must have only one order line")

        
        if(self.order_line.product_id.categ_id.name != 'Motorcycle'):
            raise ValidationError("The product added doesn't have the motorcycle category")

        # Crear aplicación de pr éstamo
        loan_application = self.env['loan.application'].create({
            'name': f"Loan for {self.name}",
            'sale_order_id': self.id,
            'down_payment': self.amount_total * 0.10,
            'interest_rate': 15.0,
            'loan_term': 36,
        })
        
        # Cambiar estado
        self.write({
            'state': 'loan_pending',
            'is_financed': True
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'loan.application',
            'res_id': loan_application.id,
            'view_mode': 'form',
            'target': 'current',
        }

        # TODO: Revisar error cuando usuario sin permisos en Motorcycle Financing entra a una Quotation
        # TODO: Revisar del 2.4 en adelante, basarse en logica del metodo apply_loan
