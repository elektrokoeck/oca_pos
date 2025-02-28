# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "POS Lot Barcode",
    "summary": "Scan barcode to enter lot/serial numbers",
    "version": "18.0.1.0.2",
    "development_status": "Alpha",
    "category": "Sales/Point of Sale",
    "website": "",
    "author": "Koeck",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        'views/pos_config_settings_views.xml',
    ],
    "depends": [
        "point_of_sale",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_lot_barcode/static/src/js/**/*",
        ],
        "web.assets_tests": [
            "pos_lot_barcode/static/tests/tours/**/*",
        ],
    },
}
