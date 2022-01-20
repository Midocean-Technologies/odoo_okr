from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from datetime import datetime


class Timesheet(models.Model):
    _name = "timesheet.timesheet"
    _description = 'Timesheet'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.users', string='USER')
    date = fields.Date(string=" Date", default=datetime.today())
    percent = fields.Float(string='DSP Percent', compute='_get_percent')
    timesheet_ids = fields.One2many('timesheet.line', 'timesheet_id')

    def _get_percent(self):
        for rec in self:
            record_count = len(rec.timesheet_ids.mapped('id'))
            # self.percent = sum(self.timesheet_ids.mapped('status.value'))
            status_values = 0.0
            for line in rec.timesheet_ids:
                status_values += line.status_id.value

            percent_value = status_values / record_count
            percent = percent_value * 100

            rec.percent = percent


class TimesheetLine(models.Model):
    _name = "timesheet.line"
    _description = 'Timesheet Line'

    timesheet_id = fields.Many2one('timesheet.timesheet', string="Timesheet")
    start_time = fields.Datetime("Start Time")
    end_time = fields.Datetime("End Time")
    task_detail = fields.Text("Task Details")
    status_id = fields.Many2one('okr.status', "Status")
    key_result_id = fields.Many2one('key.result', 'Key Result')

    @api.model
    def create(self, vals):
        partnert_ids = self.env['timesheet.timesheet'].search([('id', '=', vals['timesheet_id'])]).mapped('partner_id')

        keyresult_ids = self.env['keyresult.report'].search([('key_result_id', '=', vals['key_result_id'])]).mapped('key_result_id.id')

        report_partner_ids = self.env['keyresult.report'].search([('key_result_id', '=', vals['key_result_id'])]).mapped('partner_id.id')

        if vals['key_result_id'] not in keyresult_ids or partnert_ids.id not in report_partner_ids:

            self.env['keyresult.report'].create(
                {
                    'partner_id': partnert_ids.id,
                    'key_result_id': vals['key_result_id'],
                }
            )
        res = super(TimesheetLine, self).create(vals)
        return res

    @api.onchange('start_time')
    def validate_today_date(self):
        if self.start_time:
            str_obj = str(self.start_time)
            print(str_obj)
            obj = datetime.strptime(str_obj, '%Y-%m-%d %H:%M:%S').date()
            if obj != self.timesheet_id.date:
                raise ValidationError("Start date must be today's date")

    @api.onchange('end_time')
    def validate_end_time(self):
        if self.end_time:
            str_obj = str(self.end_time)
            print(str_obj)
            obj = datetime.strptime(str_obj, '%Y-%m-%d %H:%M:%S').date()
            if obj != self.timesheet_id.date:
                raise ValidationError("End date must be today's date")

        if self.start_time > self.end_time:
            raise ValidationError("start time  must be less then end time")
