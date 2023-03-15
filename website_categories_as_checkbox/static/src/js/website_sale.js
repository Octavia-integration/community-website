odoo.define('website_categories_as_checkbox.website_sale', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var websiteSaleWidget = require('website_sale.website_sale');

publicWidget.registry.WebsiteSale.include({
    events: _.extend({
        'change form.js_checkboxes_categories input': '_onChangeCheckboxCat',
    }, websiteSaleWidget.prototype.events),
    /**
     * @private
     * @param {Event} ev
     */
    _onChangeCheckboxCat: function (ev) {
        if (!ev.isDefaultPrevented()) {
            ev.preventDefault();
            $(ev.currentTarget).closest("form").submit();
        }
    },
})});
