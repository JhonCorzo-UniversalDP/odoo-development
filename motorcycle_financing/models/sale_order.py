from odoo import fields, models, api
import logging
from odoo.exceptions import UserError

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

    @api.onchange('is_financed')
    def _check_sale_order_with_motorcycle_categ(self):
        for record in self:
            if(record.is_financed):
                is_valid, message = record.can_apply_loan()
                if(not is_valid):
                    record.is_financed = False
                    raise UserError(message)

    def can_apply_loan(self):
        if(len(self.order_line) > 1):
            return False, "Can't apply for an loan that has a sale order with more than one order line"

        if(self.order_line.product_id.categ_id.name != 'Motorcycle'):
            return False, "The product added doesn't have the motorcycle category"

        return True, ""

    def apply_loan(self):
        self.ensure_one()

        is_valid, message = record.can_apply_loan()

        if(not is_valid):
            raise UserError(message)


        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'loan.application',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_sale_order_id': self.id,
                'default_name': f"Loan - {self.name}",
            }
        }

        # TODO: Revisar error cuando usuario sin permisos en Motorcycle Financing entra a una Quotation
        # TODO: Revisar del 3.2.4 en adelante, basarse en logica del metodo apply_loan
