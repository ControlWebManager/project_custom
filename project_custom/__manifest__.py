{
    'name': 'Custom Project',
    'description': 'Personalizacion de aplicaccion Projecto Odoo',
    'author': 'In henry Vivas',
    'depends': ['project'],
    'application': False,
    'data': [
        'security/project_custom_security.xml',
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/project_assets.xml',
        'report/project_task_report.xml',
        'report/project_report_template.xml',
    ],
}