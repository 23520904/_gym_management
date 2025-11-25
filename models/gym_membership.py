# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta

class GymMembership(models.Model):
    _name = 'gym.membership'
    _description = 'Thẻ Hội Viên Gym'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Mã thẻ', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Hội viên', required=True)
    active = fields.Boolean(default=True, string="Còn hiệu lực")
    
    product_id = fields.Many2one('product.product', string='Gói đăng ký', required=True)
    
    start_date = fields.Date(string='Ngày bắt đầu', default=fields.Date.context_today)
    end_date = fields.Date(string='Ngày hết hạn')
    
    # --- ĐÃ XÓA group_expand='_expand_states' ĐỂ CHẠY ĐƯỢC ---
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('active', 'Đang hoạt động'),
        ('frozen', 'Đang bảo lưu'),
        ('expired', 'Hết hạn'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft')

    total_sessions = fields.Integer(string='Tổng buổi', default=0)
    remaining_sessions = fields.Integer(string='Buổi còn lại', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('gym.membership') or _('New')
        return super(GymMembership, self).create(vals_list)

    @api.onchange('product_id', 'start_date')
    def _onchange_product_duration(self):
        if self.product_id and self.start_date:
            # Logic đơn giản hóa để tránh lỗi field bên product chưa có
            # Tạm thời cộng cứng 30 ngày để test luồng chạy
            self.end_date = self.start_date + relativedelta(days=30)

    def action_confirm(self):
        self.write({'state': 'active'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_freeze(self):
        self.write({'state': 'frozen'})