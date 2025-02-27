from odoo import models, fields, api, _
from odoo import Command
from odoo.exceptions import UserError

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        models = super()._load_pos_data_models(config_id)
        if "stock.lot" not in models:
            models.append("stock.lot")
        return models

    def find_product_by_id(self, product_id, config_id):

        product_fields = self.env["product.product"]._load_pos_data_fields(config_id)
        product_context = {**self.env.context, "display_default_code": False}

        product = self.env["product.product"].search([
            ("id", "=", product_id),
            ("sale_ok", "=", True),
            ("available_in_pos", "=", True),
        ], limit=1)

        if product:
            return {"product.product": product.with_context(product_context).read(product_fields, load=False)}

        return {"product.product": []}

    def find_lot_by_name(self, lot_name, config_id):
        #lot_fields = self.env["stock.lot"].fields_get().keys()
        lot_fields = ["id", "name", "product_id"]
        lot_context = {**self.env.context, "display_default_code": False}

        lot = self.env["stock.lot"].search([
            ("name", "=", lot_name),
        ], limit=1)

        if lot:
            return {"stock.lot": lot.with_context(lot_context).read(lot_fields, load=False)}

        return {"stock.lot": []}

