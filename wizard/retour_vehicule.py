from odoo import fields, models, api, _
import logging

_logger = logging.getLogger(__name__)


class RetourVehicule(models.Model):
    _name = 'retour.vehicule'
    _description = 'Table des retour vehicule'

    immatriculation = fields.Char(string="Immatriculation du vehicule", required=True)
    vehicule_ids = fields.Many2many('nom.vehicule', string="Etudiant", compute='get_vehicule')

    @api.onchange('immatriculation')
    def get_vehicule(self):
        if self.immatriculation:
            vehicules = self.env['nom.vehicule'].search([('immatriculation', '=', self.immatriculation),
                                                         ('state', '=', 'loue')
                                                         ])
            self.vehicule_ids = vehicules

    def retour_vehicule(self):
        vehicules = self.env['nom.vehicule'].search([('id', '=', self.vehicule_ids.id)])
        _logger.info("############## ####### ####### UPDATE DATE ")
        _logger.info(vehicules)
        date_data = {
            'state': 'ouvert',
            'ouvert': True,
            'cloturer': False,
            'brouillon': False,
        }
        vehicules.update(date_data)
