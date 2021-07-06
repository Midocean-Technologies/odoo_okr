from odoo import api, fields, models,_
from odoo.exceptions import ValidationError,RedirectWarning,UserError
import re
from datetime import datetime, timedelta
from datetime import datetime, timedelta

class Objective(models.Model):
    _name= "objective.objective"
    _description='objective'
    _rec_name = 'objective_title_id'
    
 
    objective_title_id = fields.Char(string='Objective Title')
    start_date = fields.Date(string="Starting Date",default=datetime.today())
    end_date = fields.Date(string="Ending Date")
    total_hour = fields.Float(string='Total Hours')
    progress = fields.Float(string='Progress %')
    purpose = fields.Char(string='Purpose')
    remark = fields.Text(string='Remarks')
    objective_ids = fields.One2many('objective.line' ,'objective_id')



class ObjectiveLine(models.Model):
    _name = "objective.line"
    _description='ObjectiveLine'

    objective_id = fields.Many2one('objective.objective',string="Objective")
    key_result = fields.Many2one('key.result',"Key Result")
    employee = fields.Many2one('res.partner',"Employee")
    progress = fields.Float(string='Progress %')
    total_hour = fields.Float(string='Total Hours')
    
    
    


   

    


 

