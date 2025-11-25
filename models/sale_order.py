# -*- coding: utf-8 -*-
from odoo import models, api, fields
class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        Override hàm Confirm của Sale Order.
        Sau khi confirm đơn hàng, quét các dòng sản phẩm.
        Nếu thấy sản phẩm Gym -> Tạo thẻ hội viên tương ứng.
        """
        # 1. Gọi hàm gốc của Odoo để xác nhận đơn hàng như bình thường
        res = super(SaleOrder, self).action_confirm()

        # 2. Logic custom: Tạo thẻ Gym
        for order in self:
            for line in order.order_line:
                # Kiểm tra xem sản phẩm có phải là loại Gym không
                # (Dựa vào field gym_product_type mình đã thêm bên Product)
                if line.product_id.gym_product_type:
                    
                    # Tạo record trong gym.membership
                    self.env['gym.membership'].create({
                        'partner_id': order.partner_id.id,
                        'product_id': line.product_id.id,
                        'start_date': fields.Date.context_today(self), # Mặc định bắt đầu từ hôm nay
                        # Các field end_date, total_sessions sẽ tự tính nhờ logic onchange/compute bên model Membership
                        'name': 'New', # Để trigger sequence sinh mã tự động
                        'state': 'draft', # Để nháp cho Lễ tân kích hoạt sau, hoặc 'active' luôn tùy bạn
                    })
                    
        return res