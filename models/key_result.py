from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, RedirectWarning, UserError
import re


class Key(models.Model):
    _name = "key.result"
    _description = 'Key Result'
    _rec_name = 'title'

    title = fields.Char(string='Key Result Title')
    partner_id = fields.Many2one('res.users', string='USER')
    hours = fields.Float(string='Hours', compute='_get_hours')
    key_result_progress = fields.Float(string='Key Result Progress', compute='_get_key_result_progress')

    def _get_key_result_progress(self):
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
                rec.key_result_progress = final_value
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
                rec.key_result_progress = final_value

    def _get_hours(self):
        for rec in self:
            lines = self.env['timesheet.line'].search([('key_result_id.id', '=', rec.id)])
            get_record_hours = []
            for line in lines:
                get_record_hours.append((line.end_time - line.start_time).total_seconds())
            sum_of_record_hours = sum(get_record_hours)
            hours = round(sum_of_record_hours / 3600, 2)
            rec.hours = hours
