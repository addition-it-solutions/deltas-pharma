# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Addition IT Solutions Pvt. Ltd. (<http://www.aitspl.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _

class addsol_region_state(models.Model):
    _name = 'addsol.region.state'
    description = "Region against State"
    
    name = fields.Char("Region Name", required=True)
    state_id = fields.Many2one('res.country.state', "State")
    partner_id = fields.Many2one('res.partner', "Stockist")
    comment = fields.Text("Notes")
    

class addsol_mr_region_mapping(models.Model):
    _name = 'mr.region.mapping'
    description = "Mapped MR with region"
    
    user_id = fields.Many2one('res.users', "MR", default=lambda self: self.env.user)
    state_id = fields.Many2one('res.country.state', "State")
    region_ids = fields.Many2many('addsol.region.state', string="Region")
