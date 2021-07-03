from odoo import api, fields, models,_
from odoo.exceptions import ValidationError,RedirectWarning,UserError
import re

class Timesheet(models.Model):
    _name= "timesheet.timesheet"
    _description='Timesheet'
    _rec_name = 'employee_id'


    company = fields.Char(string='Company')
    employee = fields.Char(string='Employee')
    employee_id = fields.Many2one('res.partner',string='Employee Name')
    date = fields.Date(string=" Date")
    percent = fields.Float(string='DSP Percent')
    timesheet_ids = fields.One2many('timesheet.line' ,'timesheet_id')
   


class TimesheetLine(models.Model):
    _name = "timesheet.line"
    _description='Timesheet Line'

    timesheet_id = fields.Many2one('timesheet.timesheet',string="Timesheet")
    start_time = fields.Float("Start Time")
    end_time = fields.Float("End Time")
    status = fields.Many2one('okr.status',"Status")
    key_result = fields.Char('Key Result')

   

   
