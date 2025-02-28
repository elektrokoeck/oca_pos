from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_enable_lot_serial_scanning = fields.Boolean(
        string="Enable Lot & Serial Number Scanning",
        related="pos_config_id.module_enable_lot_serial_scanning", readonly=False
    )

    pos_load_lots_from_cache = fields.Boolean(
        string="Load Lot/Serial Numbers from Cache",
        related="pos_config_id.module_load_lots_from_cache", readonly=False

    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        pos_enable_lot_serial_scanning = icp_sudo.get_param('res.config.settings.pos_enable_lot_serial_scanning')
        pos_load_lots_from_cache = icp_sudo.get_param('res.config.settings.pos_load_lots_from_cache')
        res.update(
            pos_enable_lot_serial_scanning=pos_enable_lot_serial_scanning,
            pos_load_lots_from_cache=pos_load_lots_from_cache,
        )
        return res
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.pos_enable_lot_serial_scanning', self.pos_enable_lot_serial_scanning)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.pos_load_lots_from_cache', self.pos_load_lots_from_cache)
        return res