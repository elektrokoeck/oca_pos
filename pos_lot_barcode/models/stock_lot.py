from odoo import models, api

class StockLot(models.Model):
    _name = "stock.lot"
    _inherit = ["stock.lot", "pos.load.mixin"]

    @api.model
    def _load_pos_data_domain(self, data):
        """ Definiert die Domain für das Laden von Lots in POS """
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
        fields = list(set(self._load_pos_data_fields(data["pos.config"]["data"][0]["id"])))

        domain = self._load_pos_data_domain(data)
        lots = self.env['stock.lot'].search_read(domain, fields, order="create_date DESC", load=False)

        return {
            "data": lots,
            "fields": fields,
        }
