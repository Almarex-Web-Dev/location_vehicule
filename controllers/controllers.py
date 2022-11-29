# -*- coding: utf-8 -*-
# from odoo import http


# class Location(http.Controller):
#     @http.route('/location/location/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/location/location/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('location.listing', {
#             'root': '/location/location',
#             'objects': http.request.env['location.location'].search([]),
#         })

#     @http.route('/location/location/objects/<model("location.location"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('location.object', {
#             'object': obj
#         })
