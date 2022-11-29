# coding=utf-8
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


STATE_TYPE_PRO_LOCA = [
    ('proprietaire', ("Propriétaire")),
    ('locataire', ("Locataire"))
]

class Acteurs_location(models.Model):
    _inherit = 'res.partner'

    proprietaire_locataire = fields.Selection(STATE_TYPE_PRO_LOCA,string="Statut")
    type_piece_locataire = fields.Many2one('type.piece', string="Type de pièce")
    numero_piece_locataire = fields.Char(string="Numéro de pièce")