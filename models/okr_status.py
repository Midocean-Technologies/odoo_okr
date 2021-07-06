from odoo import api, fields, models,_
from odoo.exceptions import ValidationError,RedirectWarning,UserError
import re

class Status(models.Model):
    _name= "okr.status"
    _description='Status'
    _rec_name = 'status'
 
    status = fields.Char(string='Status')
    value = fields.Float(string='Add Value')
    
    

   

   
