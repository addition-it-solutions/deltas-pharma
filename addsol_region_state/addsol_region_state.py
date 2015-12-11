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
    comment = fields.Text("Notes")
    
    

class dr_qualification(models.Model):
    _name = 'dr.qualification'
    _description = "Doctor's Qualification"
    
    name = fields.Char("Name", required=True)
    

class dr_speciality(models.Model):
    _name = 'dr.speciality'
    description = "Doctor's Speciality"
    
    name = fields.Char("Name", required=True)
    
    
class product_template(models.Model):
    _inherit = 'product.template'
    
    promotional_material = fields.Boolean("Promotional Material", help="check this if product is promotional material")
    brochure = fields.Boolean("Brochure", help="check this if product is brochure")
    catalogs = fields.Boolean("Catalogs", help="check this if product is catalogs")
    
    
    
class addsol_res_users(models.Model):
    _inherit = 'res.users'
    
    region_id = fields.Many2one('addsol.region.state', "Default Region")
    

class addsol_res_partner(models.Model):
    _inherit = 'res.partner'
    
    superstockist = fields.Boolean("SuperStockist", help="Check this box if this contact is a Superstockist")
    stockist = fields.Boolean("Stockist", help="Check this box if this contact is a Stockist.")
    chemist = fields.Boolean("Chemist", help="Check this box if this contact is a Chemist.")
    doctor = fields.Boolean("Doctor", help="Check this box if this contact is a Doctor.")
    qual_ids = fields.Many2many('dr.qualification', 'res_partner_qualification', 'res_partner_qual_id', 'dr_qualification_id', string='Qualification')
    spec_ids = fields.Many2many('dr.speciality', 'res_partner_speciality', 'res_partner_spec_id', 'dr_speciality_id', string='Speciality')
    region_ids = fields.Many2many('addsol.region.state', 'res_partner_region', 'res_partner_region_id', 'addsol_region_state_id', string="Region")
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        res = {}
        list_ids = []
        res = super(addsol_res_partner, self).search(args=args, offset=offset, limit=limit, order=order, count=count)
        part_id = self._context.get('partner_id')
        chemist = self._context.get('default_chemist')
        stockist = self._context.get('default_stockist')
        
        if (chemist == 1 and stockist == 0) or (chemist == 0 and stockist == 1):
            for p_id in self.browse(part_id):
                doctor_reg_id = p_id.region_ids.id
                for b_id in res:
                    chemist_reg_id = b_id.region_ids.id
                    if doctor_reg_id == chemist_reg_id:
                        list_ids.append(b_id.id)
                        
            return self.browse(list_ids)
        else:
            return res
                
        #if reg_id == chemist_reg_id:
            
        #return res
    
class doctor_chemist_mapping(models.Model):
    _name = 'doctor.chemist.mapping'
    
    dr_partner_id = fields.Many2one('res.partner', "Doctor")
    doctor_chemist_mapping_ids = fields.One2many('doctor.chemist.mapping.line', 'doctor_chemist_mapping_id', "Chemist")
    
    
class doctor_chemist_mapping_line(models.Model):
    _name = 'doctor.chemist.mapping.line'
    
    doctor_chemist_mapping_id = fields.Many2one('doctor.chemist.mapping')
    chemist_partner_id = fields.Many2one('res.partner', "Chemist")
    preferred_flag = fields.Boolean("Preferred")
    
    
class stockist_chemist_mapping(models.Model):
    _name = 'stockist.chemist.mapping'
    
    stockist_partner_id = fields.Many2one('res.partner', "Stockist")
    stockist_chemist_mapping_ids = fields.One2many('stockist.chemist.mapping.line', 'stockist_chemist_mapping_id', "Chemist")
    
    
class stockist_chemist_mapping_line(models.Model):
    _name = 'stockist.chemist.mapping.line'
    
    stockist_chemist_mapping_id = fields.Many2one('stockist.chemist.mapping')
    chemist_partner_id = fields.Many2one('res.partner', "Chemist")
    
    
class super_stockist_mapping(models.Model):
    _name = 'super.stockist.mapping'
     
    super_partner_id = fields.Many2one('res.partner', "SuperStockist")
    super_stockist_mapping_ids = fields.One2many('super.stockist.mapping.line', 'super_stockist_mapping_id', "Stockist")
     
     
class super_stockist_mapping_line(models.Model):
    _name = 'super.stockist.mapping.line'
     
    super_stockist_mapping_id = fields.Many2one('super.stockist.mapping')
    stockist_partner_id = fields.Many2one('res.partner', "Stockist")
    

class scheme_product(models.Model):
    _name = 'scheme.product'
     
    name = fields.Char("Name")
    descprition = fields.Text("Description")
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")
    scheme_region_ids = fields.One2many('scheme.product.region.line', 'region_scheme_product_id', "Region")
    scheme_product_ids = fields.One2many('scheme.product.product.line', 'scheme_product_product_id', "Product")
     
class scheme_product_region_line(models.Model):
    _name = 'scheme.product.region.line'
     
    region_scheme_product_id = fields.Many2one('scheme.product')
    addsol_region_state_id = fields.Many2one('addsol.region.state', "Region")
     
class scheme_product_product_line(models.Model):
    _name = 'scheme.product.product.line'
      
    scheme_product_product_id = fields.Many2one('scheme.product')
    product_id = fields.Many2one('product.product', "Product")

