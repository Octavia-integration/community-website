# © 2022 Nico Darnis
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Show Website Description",
    "category": "Website",
    "summary": "Module to Show Website Description in Backend",
    "website": "https://www.niboo.com/",
    "version": "16.0.1.0.1",
    "license": "AGPL-3",
    "description": """
    Allow html description edition in the product back-end instead of with the website editor

    """,
    "author": "Niboo",
    "depends": [
        "product",
        "website_sale",
    ],
    "data": [
        "views/product.xml",
    ],
    "installable": True,
    "application": False,
}
