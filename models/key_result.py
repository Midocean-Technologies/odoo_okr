from odoo import api, fields, models,_
from odoo.exceptions import ValidationError,RedirectWarning,UserError
import re

class Key(models.Model):
    _name= "key.result"
    _description='Key Result'
    _rec_name = 'key_result_title'
    
    key_result_title = fields.Char(string='Key Result Title')
    key_result_progress = fields.Float(string='Key Result Progress ')
    employee = fields.Many2one('res.partner',string='Employee')
    employee_id = fields.Many2one('res.partner',string='Employee Name')
    

   

   
