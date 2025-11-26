from odoo import models, api, fields
class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                if line.product_id.gym_product_type:
                    self.env['gym.membership'].create({
                        'partner_id': order.partner_id.id,
                        'product_id': line.product_id.id,
                        'start_date': fields.Date.context_today(self), 
                        'name': 'New', 
                        'state': 'draft',
                    })       
        return res