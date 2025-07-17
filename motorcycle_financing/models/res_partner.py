from odoo import models,fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    application_ids = fields.One2many(
        comodel_name='loan.application',
        inverse_name='partner_id',
        string='Loan Applications'
    )

    application_count = fields.Integer(
        string="Application Count",
        compute="_compute_application_count"
    )

    @api.depends('application_ids')
    def _compute_application_count(self):
        for record in self:
            record.application_count = len(record.application_ids)


    def action_view_applications(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'loan.application',
            'view_mode': 'list,form',
            'target': 'current',
            'name': f'Loan Applications - {self.name}',
            # ? Se pasa el dominio de la vista
            'domain': [('partner_id', '=', self.id)],
            # ? Se pasa el contexto para crear nuevas aplicaciones de prestamo
            'context': [('default_partner_id', '=', self.id)]

        }