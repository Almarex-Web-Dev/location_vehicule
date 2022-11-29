# -*- coding: utf-8 -*-
{
    'name': "location vehicule",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','portal','website', 'website_event','account'],

    # always loaded
    'data': [
        "security/security.xml",
		"security/ir.model.access.csv",
		"views/menu.xml",
        'views/location.xml',
        'views/acteurs.xml',
        'views/vehicule.xml',
        'views/configurations.xml',
        'views/templates.xml',
        'views/account_view.xml',
        'template/accueil.xml',
        'report/report_format_papier.xml',
        'report/report_location_vehicule.xml',
        'data/sequence.xml',
        'wizard/retour_vehicule.xml',
        'data/website.menu.csv',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
