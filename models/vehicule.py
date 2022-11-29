# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)

STATE_TYPE_PRO_LOCA = [
    ('proprietaire', ("Propriétaire")),
    ('locataire', ("Locataire"))
]

TYPE_CARBURANT = [
    ('essence', ("Essence")),
    ('diesel', ("Diesel")),
    ('electric', ("Electrique")),
    ('hybrid', ("Hybride"))
]

TRANSMISSION = [
    ('manual', ("Manuelle")),
    ('automatic', ("Automatique"))
]

STATES = [('brouillon', 'Brouillon'), ('ouvert', 'Ouvert'), ('loue', 'Déja loué')]


class NomVehicule(models.Model):
    _name = 'nom.vehicule'
    _description = "Vehicule"

    @api.depends('immatriculation', 'marque_vehicule_id', 'modele_vehicule_id')
    def _compute_name(self):
        for vehicle in self:
            names = [vehicle.marque_vehicule_id.name, vehicle.modele_vehicule_id.name, vehicle.immatriculation]
            vehicle.name = ' '.join(filter(None, names))

    def get_vehicule_name(self):
        vehicles = self.env['nom.vehicule'].search([])
        print("ve", vehicles)
        for vehicle in vehicles:
            vehicle._compute_name()
            print(vehicle.name)

    name = fields.Char(string="Véhicule", compute=_compute_name, store=True)
    immatriculation = fields.Char(string="Immatriculation")
    marque_vehicule_id = fields.Many2one('marque.vehicule', string="Marque")
    modele_vehicule_id = fields.Many2one('modele.vehicule', string="Modèle")
    type_carburant = fields.Selection(TYPE_CARBURANT, string="Type carburant")
    couleur_vehicule = fields.Char(string="Couleur")
    nbre_siege = fields.Integer(string="Nbre siège")
    nbre_portiere = fields.Integer(("Nbre portière"))
    transmission = fields.Selection(TRANSMISSION, string="Transmission")
    date_fin_assurance = fields.Date(("Fin assurance"))
    date_fin_visite = fields.Date(("Fin visite"))
    active = fields.Boolean("Active", default=True)
    kilometrage = fields.Integer(("Kilométrage (km/h)"))
    proprietaire = fields.Many2one('res.partner', string="Proprietaire",
                                   domain=[('proprietaire_locataire', '=', 'proprietaire')])
    montant_journalier = fields.Float(string="Montant journalier")
    ville = fields.Many2one('nom.ville', string="Ville")
    state = fields.Selection(selection=STATES, readonly=True, default='brouillon', string="State", help="")
    ouvert = fields.Boolean("OUVERT", default=False)
    cloturer = fields.Boolean("CLOTURER", default=False)
    brouillon = fields.Boolean("BROUILLON", default=False)
    image = fields.Binary(string="Image", max_width=150, max_heigth=140, widget="photo")
    image1 = fields.Binary(string="Image 1")
    image2 = fields.Binary(string="Image 2")
    image3 = fields.Binary(string="Image 3")
    image4 = fields.Binary(string="Image 4")
    image5 = fields.Binary(string="Image 1")
    image6 = fields.Binary(string="Image 2")
    image7 = fields.Binary(string="Image 3")
    image8 = fields.Binary(string="Image 4")

    _sql_constraints = [(
        'vehicule_unique',
        'UNIQUE (immatriculation)',
        'Ce vehicule existe déjà!'
    )]

    def action_draft(self):
        self.state = 'brouillon'
        self.brouillon = True
        self.ouvert = False
        self.cloturer = False

    def action_confirm(self):
        self.state = 'ouvert'
        self.ouvert = True
        self.cloturer = False
        self.brouillon = False

    def action_done(self):
        self.state = 'loue'
        self.cloturer = True
        self.ouvert = False
        self.brouillon = False
