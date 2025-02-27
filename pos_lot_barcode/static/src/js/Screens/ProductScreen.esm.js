/** @odoo-module **/

/*
    Copyright 2022 Camptocamp SA
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
*/
import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";
import {patch} from "@web/core/utils/patch";
import {useBarcodeReader} from "@point_of_sale/app/barcode/barcode_reader_hook";
import { useService } from "@web/core/utils/hooks";
import { WarningDialog } from "@web/core/errors/error_dialogs";
import { _t } from "@web/core/l10n/translation";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        useBarcodeReader({
            lot: this._barcodeLotAction,
        });
    },
    async _barcodeLotAction(code) {
        const product = await this._getProductByLotBarcode(code);
        if (!product) {
            return;
        }
        let order = this.pos.get_order();
        let existingLot = order.get_orderlines().some(line =>
            line.pack_lot_ids && line.pack_lot_ids.some(lot => lot.lot_name === code.code)
        );
        if (existingLot) {
            this.dialog.add(WarningDialog, {
                title: _t("Warning: lot/serial error"),
                message: _t(`lot/serial '"${code.code}"' exists already in order`),
            });
            return;
        }
        await this.pos.addLineToCurrentOrder({ product_id: product }, { code: code });
        this.numberBuffer.reset();
    },

    async _getProductByLotBarcode(code) {
        let  stock_lot = null;
        let  product = null;
        if (this.pos.models["stock.lot"])
        {
            stock_lot = this.pos.models["stock.lot"].find(lot => lot.name === code.code);
        }
        if (!stock_lot) {
            const result = await this.pos.data.callRelated(
                "pos.session",
                "find_lot_by_name",
                [odoo.pos_session_id, code.code, this.pos.config.id]
            );

            if (result && result["stock.lot"].length > 0) {
                    stock_lot = result["stock.lot"][0];
            } else {
                this.barcodeReader.showNotFoundNotification(code);
                return;
            }
        }
        if (!stock_lot) {
            this.barcodeReader.showNotFoundNotification(code);
            return;
        }

        product = await this.pos.models["product.product"].getBy("id", stock_lot.product_id.id);

        if (!product) {
            const records = await this.pos.data.callRelated(
                "pos.session",
                "find_product_by_id",
                [odoo.pos_session_id, stock_lot.product_id.id, this.pos.config.id]
            );

            if (records && records["product.product"].length > 0) {
                    product = records["product.product"][0];
            }
        }

        return product;
    }

});
