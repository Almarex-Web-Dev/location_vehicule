from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class MarqueVehicule(models.Model):
    _name = 'marque.vehicule'
    _description = "Marque"

    name = fields.Char(string="Marque", required=True)

    @api.onchange('name')
    def capitalize_name(self):
        if self.name:
            self.name = self.name.upper()

    _sql_constraints = [
        ('name', 'unique (name)', 'Le véhicule existe déja!')
    ]


class ModeleVehicule(models.Model):
    _name = 'modele.vehicule'
    _description = "Modele vehicule"

    name = fields.Char(("Modèle"), required=True)
    marque_id = fields.Many2one('marque.vehicule', string=("Marque"), required=True)



class TypePiece(models.Model):
    _name = 'type.piece'
    _description = "Table de configuration des pièce d'identité"
    _rec_name = 'name'

    name = fields.Char(string="Type de pièce d'identité")



class NomVille(models.Model):
    _name = 'nom.ville'
    _description = "Table de configuration des villes"

    name = fields.Char(string="Ville")