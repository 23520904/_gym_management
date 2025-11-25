# -*- coding: utf-8 -*-
{
    'name': "Gym Management System",
    'summary': """
        Quản lý phòng Gym, Hội viên, Gói tập và Check-in
    """,
    'description': """
        Module quản lý phòng Gym toàn diện:
        - Quản lý vòng đời hội viên (Đăng ký, Gia hạn, Hủy).
        - Cấu hình gói tập (Thời gian, Số buổi).
        - Tích hợp bán hàng (Sale Order).
        - Check-in và kiểm soát ra vào.
        - Tính năng bảo lưu thẻ.
    """,
    'author': "IS336 nhom 11",
    'website': "uit.edu.vn",
    'category': 'Services/Gym',
    'version': '19.0.1.0.0',
    
    # Các module bắt buộc phải có
    'depends': [
        'base', 
        'sale_management',  # Để tích hợp bán hàng
        'product',          # Để cấu hình gói tập
        'mail',             # Để chat và log lịch sử
    ],

    # Danh sách file dữ liệu (Load theo thứ tự)
    'data': [
        'security/gym_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/product_views.xml',
        'views/gym_membership_views.xml',
        'views/menus.xml',
    ],

    # Odoo 19 Assets (Frontend/Backend JS & CSS)
    'assets': {
        'web.assets_backend': [
            # Sau này sẽ thêm file CSS/JS custom tại đây
        ],
    },
    
    'installable': True,
    'application': True, 
    'license': 'LGPL-3',
}