from odoo import api, fields, models, _


class KeyResultReports(models.Model):
    _name = "keyresult.report"
    _description = 'KeyResult Report'

    partner_id = fields.Many2one('res.users', string='User')
    key_result_id = fields.Many2one('key.result', string='Key Result')
    hours = fields.Float(string='Hours', compute='_get_hours')

    @api.model
    def create(self, vals):
        res = super(KeyResultReports, self).create(vals)
        return res

    def _get_hours(self):
        for rec in self:
            lines = self.env['timesheet.line'].search([('key_result_id.id', '=', rec.key_result_id.id)])
            get_record_hours = []
            for line in lines:
                get_record_hours.append((line.end_time - line.start_time).total_seconds())
            sum_of_record_hours = sum(get_record_hours)
            hours = round(sum_of_record_hours / 3600, 2)
            rec.hours = hours


class ObjectiveReport(models.Model):
    _name = 'objective.report'
    _description = 'Objective Report'

    partner_id = fields.Many2one('res.users', string='User')
    objective_id = fields.Many2one('objective.objective', string='Objective')
    hours = fields.Float(string='Hours', compute='_get_hours_objective_report')

    def _get_hours_objective_report(self):
        for rec in self:
            total_hours_list = self.env['objective.line'].search(
                [('partner_id', '=', rec.partner_id.id), ('objective_id', '=', rec.objective_id.id)]).mapped(
                'total_hour')
            rec.hours = sum(total_hours_list)
