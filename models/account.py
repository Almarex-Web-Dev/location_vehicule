# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import time
import pytz
import calendar

from datetime import datetime, date, timedelta
import logging
import datetime


_logger = logging.getLogger(__name__)



class AcountMove(models.Model):
    _inherit = 'account.move'

    # Ces méthodes permettente de recuperer les données en context par la génération des factures
    def _get_location(self):
        return self._context.get('location_id')

    annee = fields.Char(string="Année", default=datetime.date.today().strftime("%Y"))

    bol_location = fields.Boolean()
    bol_reservation = fields.Boolean()

    location_id = fields.Many2one('location.vehicule',string="Location")


    # @api.onchange('location_id')
    # def onchange_location(self):
    #     for record in self:
    #         if record.location_id:
    #             record.bien  = record.location_id.biens
    #             record.partner_id = record.location_id.locataire
    #             record.locataire = record.location_id.locataire
