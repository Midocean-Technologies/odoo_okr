from odoo import api, fields, models,_
from odoo.exceptions import ValidationError,RedirectWarning,UserError
import re

class Key(models.Model):
    _name= "key.result"
    _description='Key Result'
    _rec_name = 'title_id'
 
    key_result_progress = fields.Float(string='Key Result Progress ')
    employee = fields.Many2one('res.partner',string='USER')
    title_id = fields.Char(string='Key Result Title')
    

   

   
