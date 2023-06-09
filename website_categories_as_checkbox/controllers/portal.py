# © 2021 Alexandre Dutry
# © 2021 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary.

from odoo import http
from odoo.http import request

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import TableCompute, WebsiteSale

from werkzeug.exceptions import NotFound


@http.route([  # noqa: C901
    """/shop""",
    """/shop/page/<int:page>""",
    """/shop/category/<model("product.public.category"):category>""",
    """/shop/category/<model("product.public.category"):category>/page/<int:page>""",
], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
def shop(self, page=0, category=None, search='', ppg=False, **post):
    """
    I copy pasted most of the function as there was no other way to inherit
    it to do what was needed.
    What was done was to modify the search on category in order to be able
    to search on more than one category
    """
    add_qty = int(post.get('add_qty', 1))
    Category = request.env['product.public.category']
    if category:
        category = Category.search([('id', '=', int(category))], limit=1)
        if not category or not category.can_access_from_current_website():
            raise NotFound()
    else:
        category = Category

    # Modifications start here
    check_categ_list = request.httprequest.args.getlist('check_categ')
    check_categ_set = {}
    if check_categ_list:
        check_categ_ids = [int(c) for c in check_categ_list]
        check_categ_set = {int(c) for c in check_categ_list}
    # end modifs

    if ppg:
        try:
            ppg = int(ppg)
            post['ppg'] = ppg
        except ValueError:
            ppg = False
    if not ppg:
        ppg = request.env['website'].get_current_website().shop_ppg or 20

    ppr = request.env['website'].get_current_website().shop_ppr or 4

    attrib_list = request.httprequest.args.getlist('attrib')
    attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
    attributes_ids = {v[0] for v in attrib_values}
    attrib_set = {v[1] for v in attrib_values}

    domain = self._get_search_domain(search, category, attrib_values)

    # Start modif
    if check_categ_list:
        domain.append(('public_categ_ids', 'child_of', check_categ_ids))
    # End modifs

    keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))

    pricelist_context, pricelist = self._get_pricelist_context()

    request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

    url = "/shop"
    if search:
        post["search"] = search
    if attrib_list:
        post['attrib'] = attrib_list

    Product = request.env['product.template'].with_context(bin_size=True)
    search_product = Product.search(domain, order=self._get_search_order(post))
    website_domain = request.website.website_domain()
    categs_domain = [('parent_id', '=', False)] + website_domain
    if search:
        search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
        categs_domain.append(('id', 'in', search_categories.ids))
    else:
        search_categories = Category
    categs = Category.search(categs_domain)

    if category:
        url = "/shop/category/%s" % slug(category)

    product_count = len(search_product)
    pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
    offset = pager['offset']
    products = search_product[offset: offset + ppg]

    ProductAttribute = request.env['product.attribute']
    if products:
        # get all products without limit
        attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
    else:
        attributes = ProductAttribute.browse(attributes_ids)

    layout_mode = request.session.get('website_sale_shop_layout_mode')
    if not layout_mode:
        if request.website.viewref('website_sale.products_list_view').active:
            layout_mode = 'list'
        else:
            layout_mode = 'grid'

    values = {
        'search': search,
        'category': category,
        'attrib_values': attrib_values,
        'attrib_set': attrib_set,
        'pager': pager,
        'pricelist': pricelist,
        'add_qty': add_qty,
        'products': products,
        'search_count': product_count,  # common for all searchbox
        'bins': TableCompute().process(products, ppg, ppr),
        'ppg': ppg,
        'ppr': ppr,
        'categories': categs,
        'attributes': attributes,
        'keep': keep,
        'search_categories_ids': search_categories.ids,
        'layout_mode': layout_mode,
        'check_categ_set': check_categ_set,     # Modif (added)
    }
    if category:
        values['main_object'] = category
    return request.render("website_sale.products", values)
