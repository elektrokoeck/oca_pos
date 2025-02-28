from odoo import models, api

class StockLot(models.Model):
    _name = "stock.lot"
    _inherit = ["stock.lot", "pos.load.mixin"]

    @api.model
    def _load_pos_data_domain(self, data):
        return [
           # ("product_id.available_in_pos", "=", True),
           # ("product_qty", ">", 0)
        ]

    @api.model
    def _load_pos_data_fields(self, config_id):
        return [
            "name", "id", "product_id","create_date", "product_qty"
        ]

    def _load_pos_data(self, data):
        pos_config = self.env['pos.config'].browse(data['pos.config']['data'][0]['id'])
        if not pos_config.module_load_lots_from_cache:
            return {"data": [], "fields": []}

        load_lots_from_cache = self.env["ir.config_parameter"].sudo().get_param("pos_lot_barcode.load_lots_from_cache", default="False")
        if load_lots_from_cache.lower() != "true":
            return {"data": [], "fields": []}
        fields = list(set(self._load_pos_data_fields(data["pos.config"]["data"][0]["id"])))

        domain = self._load_pos_data_domain(data)
        lots = self.env['stock.lot'].search_read(domain, fields, order="create_date DESC", load=False)

        return {
            "data": lots,
            "fields": fields,
        }
