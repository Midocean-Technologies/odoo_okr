from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, RedirectWarning, UserError
import re
from datetime import datetime, timedelta
from datetime import datetime, timedelta


class Objective(models.Model):
    _name = "objective.objective"
    _description = 'Objective'

    name = fields.Char(string='Objective Title')
    start_date = fields.Date(string="Starting Date", default=datetime.today())
    end_date = fields.Date(string="Ending Date")
    total_hour = fields.Float(string='Total Hours', compute='_get_total_hours')
    progress = fields.Float(string='Progress %', compute='_get_objective_percent')
    purpose = fields.Char(string='Purpose')
    remark = fields.Text(string='Remarks')
    objective_ids = fields.One2many('objective.line', 'objective_id')

    def _get_objective_percent(self):
        for rec in self:
            record_count = len(rec.objective_ids.mapped('id'))
            status_values = 0.0
            for line in rec.objective_ids:
                status_values += line.progress
            if record_count == 0.00:
                percent_value = 0.0
            else:
                percent_value = status_values / record_count
            rec.progress = percent_value

    def _get_total_hours(self):
        for rec in self:
            rec.total_hour = sum(rec.objective_ids.mapped('total_hour'))


class ObjectiveLine(models.Model):
    _name = "objective.line"
    _description = 'ObjectiveLine'

    objective_id = fields.Many2one('objective.objective', string="Objective")
    key_result_id = fields.Many2one('key.result', "Key Result")
    partner_id = fields.Many2one('res.users', "USER")
    progress = fields.Float(string='Progress %', compute='_objective_key_result_progress')
    total_hour = fields.Float(string='Total Hours', compute='_objective_key_result_hours')

    @api.model
    def create(self, vals):
        objective = self.env['objective.objective'].search([('id', '=', vals['objective_id'])])

        objective_id = self.env['objective.report'].search([('objective_id', '=', vals['objective_id'])]).mapped(
            'objective_id.id')
        partner_id = self.env['objective.report'].search([('objective_id', '=', vals['objective_id'])]).mapped('partner_id.id')

        if vals['objective_id'] not in objective_id or vals['partner_id'] not in partner_id:
            self.env['objective.report'].create(
                {
                    'partner_id': vals['partner_id'],
                    'objective_id': objective.id,
                }
            )

        if vals.get('key_result_id') and vals.get('partner_id'):
            self.env['key.result'].search([('id', '=', vals['key_result_id'])]).write(
                {
                    'partner_id': vals['partner_id']
                }
            )
        res = super(ObjectiveLine, self).create(vals)
        return res

    def write(self, vals):
        if self.key_result_id.id and vals.get('partner_id'):
            self.env['key.result'].search([('id', '=', self.key_result_id.id)]).write(
                {
                    'partner_id': vals['partner_id']
                }
            )
            res = super(ObjectiveLine, self).write(vals)
            return res

    def _objective_key_result_progress(self):
        for rec in self:
            get_record_count = len(self.env['timesheet.line'].search([('key_result_id.id', '=', rec.id)]).mapped('id'))
            lines = self.env['timesheet.line'].search([('key_result_id.id', '=', rec.id)])
            task_records = set(
                self.env['timesheet.line'].search([('key_result_id.id', '=', rec.id)]).mapped('task_detail'))
            count_of_task = len(task_records)

            value = []
            a = []
            for record in task_records:
                check_value = self.env['timesheet.line'].search(
                    [('task_detail', '=', record), ('status_id.value', '=', 1),
                     ('key_result_id.id', '=', rec.id)]).mapped('id')
                if len(check_value) != 0:
                    value.append(len(check_value))
                    a.append(check_value[0])
            count_of_value = len(value)
            len_of_a = len(a)

            if count_of_task != count_of_value:
                get_record_value = 0.0
                for data in lines:
                    get_record_value += data.status_id.value
                if get_record_count == 0.00:
                    total_value = 0.00
                else:
                    total_value = get_record_value / get_record_count
                final_value = total_value * 100
                rec.progress = final_value
            else:
                get_record_value = 0.0
                for data in a:
                    get_record_value += sum(
                        self.env['timesheet.line'].search([('id', '=', data)]).mapped('status_id.value'))

                if len_of_a == 0.00:
                    total_value = 0.00
                else:
                    total_value = get_record_value / len_of_a
                final_value = total_value * 100
                rec.progress = final_value

    def _objective_key_result_hours(self):
        for rec in self:
            lines = self.env['timesheet.line'].search([('key_result_id.id', '=', rec.id)])
            get_record_hours = []
            for line in lines:
                get_record_hours.append((line.end_time - line.start_time).total_seconds())
            sum_of_record_hours = sum(get_record_hours)
            hours = round(sum_of_record_hours / 3600, 2)
            rec.total_hour = hours
