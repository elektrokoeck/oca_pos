from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    module_enable_lot_serial_scanning = fields.Boolean(
        string="Enable Lot & Serial Number Scanning"
    )

    module_load_lots_from_cache = fields.Boolean(
        string="Load Lot/Serial Numbers from Cache"
    )
