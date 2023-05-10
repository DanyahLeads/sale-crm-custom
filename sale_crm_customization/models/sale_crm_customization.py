from odoo import models, fields, api


class SaleCrmCustom(models.TransientModel):
    _inherit = 'crm.quotation.partner'
    trust = fields.Selection(selection=[('good', 'Good'), ('normal', 'Normal'), ('bad', 'Bad')], string="Trust")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.trust = self.partner_id.trust

    def action_apply(self):
        res = super(SaleCrmCustom, self).action_apply()
        self.lead_id.get_trust(trust_value=self.trust)
        return res


class CrmLeadTrust(models.Model):
    _inherit = 'crm.lead'
    trust = fields.Selection(selection=[('good', 'Good'), ('normal', 'Normal'), ('bad', 'Bad')], string="Trust")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.trust = self.partner_id.trust

    def action_new_quotation(self):
        res = super(CrmLeadTrust, self).action_new_quotation()
        res['context']['default_trust'] = self.trust
        return res

    def get_trust(self, trust_value=False):
        for rec in self:
            if trust_value:
                rec.trust = trust_value


class TrustSales(models.Model):
    _inherit = 'sale.order'
    trust = fields.Selection(selection=[('good', 'Good'), ('normal', 'Normal'), ('bad', 'Bad')], string="Trust")