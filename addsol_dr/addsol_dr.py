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
from datetime import date

    
class dr_qualification(models.Model):
    _name = 'dr.qualification'
    _description = "Doctor's Qualification"
    
    name = fields.Char("Name", required=True)
    

class dr_speciality(models.Model):
    _name = 'dr.speciality'
    description = "Doctor's Speciality"
    
    name = fields.Char("Name", required=True)
    

class addsol_res_partner(models.Model):
    _inherit = 'res.partner'
    
    stockist = fields.Boolean("Stockist", help="Check this box if this contact is a Stockist.")
    chemist = fields.Boolean("Chemist", help="Check this box if this contact is a Chemist.")

class dr_details(models.Model):
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
    visiting_time = fields.Char("Visiting Time")
    user_id = fields.Many2one('res.users', "Salesperson", default=lambda self: self.env.user)
    region_id = fields.Many2one('addsol.region.state', "Region")
    comment = fields.Text("Notes")
    qual_ids = fields.Many2many('dr.qualification', string="Qualification")
    spec_ids = fields.Many2many('dr.speciality', string="Speciality")
    
    
    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}


class mr_tour_plan(models.Model):
    _name = 'mr.tour.plan'
    description = "MR Tour Information"
    _rec_name = 'tour_date'
         
    employee_id = fields.Many2one('hr.employee', "MR")
    tour_date = fields.Date("Date",)
    tour_date_to = fields.Date("Date To")
    product_line_ids = fields.One2many('mr.tour.plan.line', 'tour_id', "Product", states={'draft': [('readonly', False)],'confirm': [('readonly', False)]} , readonly=True)
    state = fields.Selection([('draft', 'To Submit'), ('cancel', 'Cancelled'),('confirm', 'To Approve'), ('validate', 'Approved'), ('refuse', 'Refused')], 'Status', readonly=True)
    chemist_partner_ids = fields.Many2many('res.partner', 'mr_tour_plan_chemist' , 'mr_tour_plane_chemist_id', 'partner_id', string='Chemists', states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]} , readonly=True)
    stockist_partner_ids = fields.Many2many('res.partner', 'mr_tour_plan_stockist' , 'mr_tour_plane_stockist_id', 'partner_id', string='Stockists', states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]} , readonly=True)
     
    @api.cr_uid_ids_context
    def _employee_get(self, cr, uid, context=None):
        emp_id = context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False
     
    _defaults = {
     'state' : 'draft',
     'employee_id' : _employee_get
     }
         
    @api.one
    def plan_send(self):
        self.write({'state': 'confirm'})
        return True
         
    @api.one
    def plan_approve(self):
        self.write({'state': 'validate'})
        return True
         
    @api.one
    def refuse(self):
        self.write({'state': 'refuse'})
        return True
         
    @api.one
    def reset(self):
        self.write({'state': 'cancel'})
        return True
         
         
class mr_tour_plan_line(models.Model):
    _name = 'mr.tour.plan.line'
         
    tour_id = fields.Many2one('mr.tour.plan')
    dr_details_id = fields.Many2one('dr.details', "Doctor")
    plan_line_product_id = fields.Many2many('product.product', 'mr_tour_plan_line_product' , 'mr_tour_plane_line_id', 'product_id', string='Products')
    notes = fields.Text("Notes")
    sampling = fields.Text("Sampling")
    promotional = fields.Text("Promotional")
     