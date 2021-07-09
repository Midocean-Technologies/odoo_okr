from odoo import api, fields, models,_
from odoo.exceptions import ValidationError,RedirectWarning,UserError
import re
from datetime import datetime, timedelta

class Timesheet(models.Model):
    _name= "timesheet.timesheet"
    _description='Timesheet'
    _rec_name = 'employee'


    employee = fields.Many2one('res.partner',string='USER')
    date = fields.Date(string=" Date",default=datetime.today())
    percent = fields.Float(string='DSP Percent' ,readonly='True')
    timesheet_ids = fields.One2many('timesheet.line' ,'timesheet_id')
   


class TimesheetLine(models.Model):
    _name = "timesheet.line"
    _description='Timesheet Line'

    timesheet_id = fields.Many2one('timesheet.timesheet',string="Timesheet")
    start_time = fields.Float("Start Time" )
    end_time = fields.Float("End Time")
    task_detail = fields.Text("Task Details")
    status = fields.Many2one('okr.status',"Status")
    key_result = fields.Many2one('key.result','Key Result')

   

   
