# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta

class GymMembership(models.Model):
    _name = 'gym.membership'
    _description = 'Thẻ Hội Viên Gym'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Mã thẻ', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Hội viên', required=True, tracking=True)
    active = fields.Boolean(default=True, string="Còn hiệu lực")

    product_id = fields.Many2one('product.product', string='Gói đăng ký', required=True, tracking=True)
    start_date = fields.Date(string='Ngày bắt đầu', default=fields.Date.context_today, required=True, tracking=True)
    end_date = fields.Date(
        string='Ngày hết hạn', 
        compute='_compute_gym_info', 
        store=True, 
        readonly=False, 
        tracking=True
    )
    
    total_sessions = fields.Integer(
        string='Tổng buổi', 
        compute='_compute_gym_info', 
        store=True, 
        readonly=False
    )
    remaining_sessions = fields.Integer(string='Buổi còn lại', readonly=True)

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('active', 'Đang hoạt động'),
        ('frozen', 'Đang bảo lưu'),
        ('expired', 'Hết hạn'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='draft', tracking=True)

    @api.depends('product_id', 'start_date')
    def _compute_gym_info(self):
        for rec in self:
            end_date = rec.start_date
            total_sessions = 0
            
            if rec.product_id and rec.start_date:
                product = rec.product_id
                
                if product.gym_product_type == 'membership':
                    duration = product.gym_duration
                    unit = product.gym_duration_unit
                    if duration > 0:
                        if unit == 'day':
                            end_date = rec.start_date + relativedelta(days=duration)
                        elif unit == 'month':
                            end_date = rec.start_date + relativedelta(months=duration)
                        elif unit == 'year':
                            end_date = rec.start_date + relativedelta(years=duration)
                
                elif product.gym_product_type == 'service_pack':
                    total_sessions = product.gym_session_count
                    duration = product.gym_duration
                    if duration > 0:
                        unit = product.gym_duration_unit
                        if unit == 'day':
                            end_date = rec.start_date + relativedelta(days=duration)
                        elif unit == 'month':
                            end_date = rec.start_date + relativedelta(months=duration)
                        elif unit == 'year':
                            end_date = rec.start_date + relativedelta(years=duration)
            
            rec.end_date = end_date
            rec.total_sessions = total_sessions
            
            if not rec.id or rec.remaining_sessions == 0:
                rec.remaining_sessions = total_sessions

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('gym.membership') or _('New')
        return super(GymMembership, self).create(vals_list)

    def action_confirm(self):
        self.write({'state': 'active'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_freeze(self):
        self.write({'state': 'frozen'})
        
    @api.model
    def _cron_expire_memberships(self):
        today = fields.Date.today()
        # Tìm các thẻ đang Active mà đã quá hạn
        expired = self.search([('state', '=', 'active'), ('end_date', '<', today)])
        expired.write({'state': 'expired'})