# © 2022 Alexandre Van Ommeslaghe
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class BaseModelExtend(models.AbstractModel):
    _inherit = "base"

    def get_fields_to_hide(self):
        """
        You should inherit this method to add the fields you wish to hide in
        custom filters.
        """
        return []

    @api.model
    def fields_get(self, fields=None, attributes=None):
        fields_to_hide = self.get_fields_to_hide()
        res = super().fields_get(fields, attributes=attributes)
        for field in fields_to_hide:
            if res.get(field):
                res[field]["searchable"] = False
        return res
