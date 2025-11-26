from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    gym_product_type = fields.Selection([
        ('membership', 'Thẻ Hội Viên (Theo thời gian)'),
        ('service_pack', 'Gói Dịch Vụ (Theo buổi - PT/Yoga)'),
        ('entry', 'Vé lượt (Check-in 1 lần)')
    ], string='Loại sản phẩm Gym', help="Chọn loại để cấu hình thông số Gym tương ứng")
    gym_duration = fields.Integer(string='Thời hạn', default=1)
    gym_duration_unit = fields.Selection([
        ('day', 'Ngày'),
        ('month', 'Tháng'),
        ('year', 'Năm')
    ], string='Đơn vị tính', default='month')
    gym_session_count = fields.Integer(string='Số buổi tập', default=0, 
                                     help="Số buổi tập được cộng vào ví buổi tập của hội viên")
    @api.constrains('gym_duration', 'gym_session_count')
    def _check_gym_config(self):
        for rec in self:
            if rec.gym_product_type == 'membership' and rec.gym_duration <= 0:
                raise ValidationError(_("Thời hạn thẻ phải lớn hơn 0!"))
            if rec.gym_product_type == 'service_pack' and rec.gym_session_count <= 0:
                raise ValidationError(_("Số buổi tập phải lớn hơn 0!"))
    @api.onchange('gym_product_type')
    def _onchange_gym_product_type(self):
        if self.gym_product_type:
            self.type = 'service'
            self.invoice_policy = 'order' 