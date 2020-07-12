# -*- coding: utf-8 -*-

{
    'name': 'Project MileStones',
    'version': '13.0.1.0',
    'author': 'Technovicinfotech',
    'company': 'Technovicinfotech',
    'website': 'https://technovicinfotech.com/',
    'category': 'Project',
    'summary': 'ADD Milestones in Project',
    'description': """ ADD Milestones in Project """,
    'depends': ['sale','project','odoo_job_costing_management','account'],
    'data': [
            'security/ir.model.access.csv',
            'views/project.xml',
            'wizard/sale_advance_payment.xml'
    ],
    'installable': True,
    'auto_install': False,
}