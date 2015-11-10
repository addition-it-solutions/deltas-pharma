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

    
class addsol_dr_qualification(models.Model):
    _name = 'dr.qualification'
    _description = "Doctor's Qualification"
    
    name = fields.Char("Name", required=True)
    

class addsol_dr_speciality(models.Model):
    _name = 'dr.speciality'
    description = "Doctor's Speciality"
    
    name = fields.Char("Name", required=True)
    

class addsol_dr(models.Model):
    _name = 'dr.details'
    description = "Doctor's Information"
     
    name = fields.Char("Name", required=True)
    address1 = fields.Char("Street1")
    address2 = fields.Char("Stree2")
    zip = fields.Char("Zip", size=24, change_default=True)
    city = fields.Char("City")
    state_id = fields.Many2one('res.country.state', "State", ondelete='restrict')
    country_id = fields.Many2one('res.country', "Country", ondelete='restrict')
    email = fields.Char("Email")
    mobile = fields.Char("Mobile")
    birthdate = fields.Date("Date Of Birth")
    comment = fields.Text("Notes")
    qual_ids = fields.Many2many('dr.qualification', string="Qualification")
    spec_ids = fields.Many2many('dr.speciality', string="Speciality")
    
    
    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}
