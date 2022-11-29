# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo.http import request
import logging
import odoo.http as http
_logger = logging.getLogger(__name__)

class Accueil(http.Controller):
    @http.route('/accueil', type='http', auth="public", website=True, csrf=False)
    def location_accueil(self):
        return http.request.render('location_vehicule.accueil_location', {
            })



    @http.route('/vehicules', type='http', auth="public", website=True, csrf=False)
    def location_vehicule(self):
        vehicule = request.env['nom.vehicule'].sudo().search([
            ('state', '=', "ouvert")
        ])
        _logger.info('################ session info #############')
        _logger.info(vehicule)
        return http.request.render('location_vehicule.location_vehicule', {
                'vehicule': vehicule,
            })

    @http.route('/details/vehicule', type='http', auth="public", website=True, csrf=False)
    def location_details_vehicule(self, **post):
        _logger.info('################ POST #############')
        _logger.info(post)
        vehicule = request.env['nom.vehicule'].sudo().search([('id', '=', post.get('vehi_id'))])
        return http.request.render('location_vehicule.details_location_vehicule', {
            'vehicule': vehicule,
        })


    @http.route('/inscription/locataire', type='http', auth='public', website=True, csrf=False)
    def locataire_inscription(self, **post):
        vehicule = request.env['nom.vehicule'].sudo().search([('id', '=', post.get('vehi_id'))])
        if vehicule.state == "loue":
            return request.render('location_vehicule.desole', {
            })
        return http.request.render('location_vehicule.formulaire_locataire', {
            'vehicule': vehicule,
            'ville': request.env['nom.ville'].sudo().search([]),
            'type_piece_identite': request.env['type.piece'].sudo().search([]),
        })


    @http.route('/inscription/details', type='http', auth='public', website=True, csrf=False)
    def location_inscription_details(self, **post):
        _logger.info('################ INFORMATIONS VEHICULE #############')
        _logger.info(post)
        #raise ValidationError('Error sigleton')
        vehicule = request.env['nom.vehicule'].sudo().search([('id', '=', (post.get('vehicule')))])
        ville_id = request.env['nom.ville'].sudo().search([('id', '=', (post.get('ville')))])
        type_piece_id = request.env['type.piece'].sudo().search([('id', '=', (post.get('type_piece')))])
        if vehicule.state == "loue":
            return request.render('location_vehicule.desole', {
            })
        duree_loca = float(post.get('duree_location'))
        montant_jour = vehicule.montant_journalier
        montant_total_location = duree_loca * montant_jour
        return request.render('location_vehicule.detail_inscription_location', {
            'vehicule': vehicule,
            'ville_id': ville_id,
            'type_piece_id': type_piece_id,
            'nom': post.get('nom'),
            'prenom': post.get('prenom'),
            'email': post.get('email'),
            'contact': post.get('contact'),
            'numero_piece': post.get('numero_piece'),
            'date_debut_location': post.get('date_debut_location'),
            'date_fin_location': post.get('date_fin_location'),
            'duree_location': post.get('duree_location'),
            'montant_total_location': montant_total_location
        })


    @http.route('/validation/location', type='http', auth='public', website=True, csrf=False)
    def validation_location(self, **post):
        _logger.info('################ INFORMATIONS VEHICULE #############')
        _logger.info(post)
        #raise ValidationError('Error sigleton')
        vehicule = request.env['nom.vehicule'].sudo().search([('id', '=', (post.get('vehicule')))])
        ville_id = request.env['nom.ville'].sudo().search([('id', '=', (post.get('ville_id')))])
        type_piece_id = request.env['type.piece'].sudo().search([('id', '=', (post.get('type_piece_id')))])
        locataire_obj = request.env['res.partner']
        location_obj = request.env['location.vehicule']
        locataire = locataire_obj.sudo().search([
            ('phone', '=', post.get('contact')),
            ('email', '=', post.get('email'))
        ])
        if vehicule.state == "loue":
            return request.render('location_vehicule.desole', {
            })
        if locataire:
            values_location = {
                'vehicule_id': int(post.get('vehicule')),
                'locataire': locataire.id,
                'type_piece_locataire': int(post.get('type_piece_id')),
                'numero_piece_locataire': post.get('numero_piece'),
                'date_debut_location': post.get('date_debut_location'),
                'date_fin_location': post.get('date_fin_location'),
                'duree_location': post.get('duree_location'),
                'montant_location': post.get('montant_total_location'),
            }
            location_enreg = location_obj.sudo().create(values_location)
            vehicule.write({
                'state': "loue",
                'cloturer': True,
                'ouvert': False,
                'brouillon': False,
            })
            return request.render('location_vehicule.succes', {
                'location_enreg': location_enreg,
                'vehicule': vehicule
            })
        else:
            values_locataire = {
                'name': (post.get('nom') + " " + post.get('prenom')),
                'email': post.get('email'),
                'phone': post.get('contact'),
                'type_piece_locataire': int(post.get('type_piece_id')),
                'numero_piece_locataire': post.get('numero_piece'),
                'proprietaire_locataire': "locataire",
            }
            locataire_enreg = locataire_obj.sudo().create(values_locataire)
            values_location = {
                'vehicule_id': int(post.get('vehicule')),
                'locataire': locataire_enreg.id,
                'type_piece_locataire': int(post.get('type_piece_id')),
                'numero_piece_locataire': post.get('numero_piece'),
                'date_debut_location': post.get('date_debut_location'),
                'date_fin_location': post.get('date_fin_location'),
                'duree_location': post.get('duree_location'),
                'montant_location': post.get('montant_total_location'),
            }
            location_enreg = location_obj.sudo().create(values_location)
            vehicule.write({
                'state': "loue",
                'cloturer': True,
                'ouvert': False,
                'brouillon': False,
            })
            return request.render('location_vehicule.succes', {
                'location_enreg': location_enreg,
                'vehicule': vehicule
            })

    @http.route('/modifier/inscription/locataire', auth="public", type="http", website=True, csrf=False)
    def modifier_inscription_locataire(self, **post):
        vehicule = request.env['nom.vehicule'].sudo().search([('id', '=', (post.get('vehicule')))])
        ville_id = request.env['nom.ville'].sudo().search([('id', '=', (post.get('ville_id')))])
        type_piece_id = request.env['type.piece'].sudo().search([('id', '=', (post.get('type_piece_id')))])
        if vehicule.state == "loue":
            return request.render('location_vehicule.desole', {
            })
        return request.render('location_vehicule.modif_formulaire_locataire', {
            'vehicule': vehicule,
            'ville_id': ville_id,
            'type_piece_id': type_piece_id,
            'nom': post.get('nom'),
            'prenom': post.get('prenom'),
            'email': post.get('email'),
            'contact': post.get('contact'),
            'numero_piece': post.get('numero_piece'),
            'date_debut_location': post.get('date_debut_location'),
            'date_fin_location': post.get('date_fin_location'),
            'duree_location': post.get('duree_location'),
            'toute_ville': request.env['nom.ville'].sudo().search([]),
            'tout_type_piece': request.env['type.piece'].sudo().search([]),

        })


    @http.route('/modif/details/inscription', type='http', auth='public', website=True, csrf=False)
    def location_modif_detais_inscription(self, **post):
        _logger.info('################ INFORMATIONS #############')
        _logger.info(post)
        #raise ValidationError('Error sigleton')
        vehicule = request.env['nom.vehicule'].sudo().search([('id', '=', (post.get('vehicule')))])
        ville_id = request.env['nom.ville'].sudo().search([('id', '=', (post.get('ville')))])
        type_piece_id = request.env['type.piece'].sudo().search([('id', '=', (post.get('type_piece')))])
        if vehicule.state == "loue":
            return request.render('location_vehicule.desole', {
            })
        duree_loca = float(post.get('duree_location'))
        montant_jour = vehicule.montant_journalier
        montant_total_location = duree_loca * montant_jour
        return request.render('location_vehicule.detail_inscription_location', {
            'vehicule': vehicule,
            'ville_id': ville_id,
            'type_piece_id': type_piece_id,
            'nom': post.get('nom'),
            'prenom': post.get('prenom'),
            'email': post.get('email'),
            'contact': post.get('contact'),
            'numero_piece': post.get('numero_piece'),
            'date_debut_location': post.get('date_debut_location'),
            'date_fin_location': post.get('date_fin_location'),
            'duree_location': post.get('duree_location'),
            'montant_total_location': montant_total_location
        })

    @http.route('/gamme/fidelite', type='http', auth="public", website=True, csrf=False)
    def gamme_fidelite(self):
        return http.request.render('location_vehicule.gamme_fidelite', {
        })


    @http.route('/enreg/ligne', type='http', auth="public", website=True, csrf=False)
    def enreg_ligne(self):
        return http.request.render('location_vehicule.enreg_ligne', {
        })

