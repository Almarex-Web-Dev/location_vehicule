# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

STATE_MOYEN_PAIEMENT = [
    ('carte_credit', ("Carte de credit")),
    ('cheque', ("Chèque")),
    ('espece', ("Espèce")),
    ('virement', ("Virement bancaire")),
    ('mobile_money', ("Mobile money"))

]

STATE = [
    ('brouillon', ("Brouillon")),
    ('confirme', ("Confirmée")),
    ('cloture', ("Clôturée")),
    ('annule', ("Annulée"))
]


class LocationVehicule(models.Model):
    _name = "location.vehicule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Location de vehicule"



    name = fields.Char(("Référence"), default="Nouveau")
    locataire = fields.Many2one('res.partner', string="Locataire",
                                domain=[('proprietaire_locataire', '=', 'locataire')])
    locataire_adresse = fields.Char(related='locataire.street')
    locataire_phone = fields.Char(related='locataire.phone')
    locataire_email = fields.Char(related='locataire.email')
    locataire_name = fields.Char(related='locataire.name')
    type_piece_locataire = fields.Many2one('type.piece', string="Type de pièce")
    numero_piece_locataire = fields.Char(string="Numéro de pièce")
    nom_locataire = fields.Char(related='locataire.name', store=True)
    adresse_locataire = fields.Char(related='locataire.street', store=True)
    telephone_locataire = fields.Char(related='locataire.phone', store=True)
    state = fields.Selection(STATE, string="État", default='brouillon', tracking=1)
    brouillon = fields.Boolean("BROUILLON", default=False)
    confirme = fields.Boolean("CONFIRMER", default=False)
    cloturer = fields.Boolean("CLOTURER", default=False)
    annule = fields.Boolean("ANNULE", default=False)
    vehicule_id = fields.Many2one('nom.vehicule', string="Vehicule", tracking=1, domain=[('state', '=', 'ouvert')])
    proprietaire = fields.Many2one(related='vehicule_id.proprietaire')
    date_debut_location = fields.Date(string="Début de la date de location", tracking=1)
    date_fin_location = fields.Date(string="Fin de la date de location", tracking=1)
    duree_location = fields.Integer(string="Durée de la location")
    moyen_paiement = fields.Selection(STATE_MOYEN_PAIEMENT, string="Moyen de paiement")
    description_proprietaire = fields.Text(string="Description")
    montant_location_jour = fields.Float(related='vehicule_id.montant_journalier', string="Montant journalier")
    montant_location = fields.Float(string="Montant de la location")
    condition_particuliere = fields.Text(string="Conditions particulières")
    commentaires = fields.Text(string="Commentaires")
    invoice_ids = fields.One2many('account.move', 'location_id', string="Factures")
    test = fields.Boolean(default=False)



    @api.onchange('duree_location', 'montant_location_jour','montant_location')
    def _montant_location(self):
        for record in self:
            if record.duree_location and record.montant_location_jour:
                record.montant_location = record.montant_location_jour * record.duree_location



    @api.onchange('date_debut_location', 'date_fin_location')
    def _date_debut(self):
        for record in self:
            if record.date_fin_location and record.date_debut_location:
                if record.date_fin_location < record.date_debut_location:
                    raise ValidationError(
                        "La date du debut de location ne doit pas etre inferieure à celle de la debut de location")

    @api.model
    def create(self, values):
        values['name'] = 'LOC' + self.env['ir.sequence'].next_by_code('location.vehicule')
        result = super(LocationVehicule, self).create(values)
        return result

    def button_report_location(self):
        return self.env.ref('location.report_location_vehicule').report_action(self)

    def generate_invoice(self):
        context = self._context.copy()
        context.update({
            'location_id': self.id,
        })
        invoice_obj = self.env['account.move']
        # On va verifier si on est dans le context de location
        if context:
            # on va comparer les éléments
            loca = invoice_obj.search([
                ('partner_id', '=', self.locataire.id),
                ('location_id', '=', self.id)
            ])
            if loca:
                raise ValidationError(_("La facture de ce client pour ce vehicule a été dejà crée ."))
            else:
                # Création de la facture
                invoice_values = {
                    'move_type': 'out_invoice',
                    'currency_id': self.env.user.company_id.currency_id.id,
                    'partner_id': self.locataire.id,
                    'location_id': self.id,
                    'invoice_line_ids': [(0, 0, {
                        'name': "LOCATION " + str(self.name),
                        'price_unit': self.montant_location,
                        'quantity': 1.0,
                    })],
                }
                invoice = invoice_obj.create(invoice_values)
                res = self.sudo().env.ref('account.action_move_out_invoice_type')
                res = res.read()[0]
                res.update({
                    'domain': str([('location_id', '=', self.id)]),
                })
                return res

    def annule_bouton(self):
        self.state = 'annule'
        self.annule = True
        self.confirme = False
        self.cloturer = False

    def action_confirm(self):
        self.state = 'confirme'
        self.vehicule_id.state = 'loue'
        self.vehicule_id.cloturer = True
        self.vehicule_id.ouvert = False
        self.vehicule_id.brouillon = False
        self.confirme = True
        self.cloturer = False
        self.annule = False

    def action_cloturer(self):
        self.state = 'cloture'
        self.cloturer = True
        self.confirme = False
        self.annule = False
