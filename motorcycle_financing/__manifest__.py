{
    'name': "Motorcycle Financing",
    'summary': "Streamlines the loan application process for dealerships.",
    'description': 'Modulo encargado de llevar control sobre los prestamos realizado en Kawiil Motors',
    'category': 'Kawiil/Custom Modules',
    'version': '18.0.0.0.1',
    'website': 'https://github.com/JhonCorzo-UniversalDP/odoo-development',
    'author': "Jhon Jairo Corzo Calderon",
    'license': 'OPL-1',
    'depends': ['sale'],
	'data': [
        # Security
        'security/motorcycle_financing_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        # Views
        'views/loan_application_views.xml',
        'views/loan_application_tag_views.xml',
        'views/motorcycle_financing_menu.xml',

        # Menus

        # Data
        'data/loan_demo.xml'
    ],
    # 'demo': [
    # ],
    'application': True,
}

# ? 1. Crear Modelo
# ? 2. Crear grupos y reglas de acceso
# ? 3. Crear acciones
# ? 3. Crear menus
# ? 4. Crear vistas
# ? 5. Actualizar manifiesto


