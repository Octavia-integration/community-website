# © 2022 Alexandre Dutry, Nico Darnis
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

# TODO: Fix View when activating checkbox on website shop page options

{
    "name": "Website Product Categories as Checkbox",
    "category": "Website",
    "summary": "Website Product Categories as Checkbox",
    "website": "https://www.niboo.com/",
    "version": "14.0.1.0.1",
    "license": "AGPL-3",
    "description": """
    Show Product e-commerce categories with a checkbox to get filter the search like product variation
    """,
    "author": "Niboo",
    "depends": [
        "product",
        "website_sale",
    ],
    "data": [
        "views/website_shop_page.xml",
    ],
    "installable": False,
    "application": False,
}
