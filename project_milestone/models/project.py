# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_milestone_ids = fields.One2many('project.milestone','project_id', string="Project Milestone")
    prorate_advance_adjustment = fields.Boolean(string="Prorate Advance Adjustment", default=False, copy=False)
    total_billed = fields.Float(string="Billed")
    total_collected = fields.Float(string="Collected")
    total_remaining = fields.Float(string="Remaining")
    total_collect_percentage = fields.Float(string="Collect Percentage")
    account_id = fields.Many2one('account.account', string="Retention Account")
    collected_so_far = fields.Float(string="Collected So Far")

    def action_retention_reversal(self):
        return True


class ProjectMilestone(models.Model):
    _name = "project.milestone"


    project_id = fields.Many2one('project.project', string="Project")
    name = fields.Char(string="Milestone Name")
    percentage = fields.Char(string="Percentage")
    is_billed = fields.Boolean(string="Billed", default=False)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    milestone_ids = fields.Many2many('project.milestone','sale_order_milestones_rel', string="Milestones")
    latest_milestone_id = fields.Many2one('project.milestone', string="Latest Milestone")


class AccountInvoice(models.Model):
    _inherit = "account.move"

    milestone_id = fields.Many2one('project.milestone', string="Latest Milestone")
    advance_adjustment = fields.Float(string="Advance Adjustment")
    net_bill_customer = fields.Float(string="Net Bill Customer")
    retention = fields.Float(string="Retention")


    @api.model
    def create(self,vals):
        if 'invoice_origin' in vals and vals.get('invoice_origin'):
            sale_order = self.env['sale.order'].sudo().search([('name','=',vals.get('invoice_origin'))], limit=1)
            if sale_order and sale_order.latest_milestone_id:
                vals['milestone_id'] = sale_order.latest_milestone_id.id

        res = super(AccountInvoice, self).create(vals)
        return res

    def action_post(self):
        for move in self.filtered(lambda x: x.milestone_id):
            percentage = move.milestone_id.percentage
            invocie_amount = move.amount_total
            # if percentage:
            #     sale_order = self.env['sale.order'].sudo().search([('name','=',move.invoice_origin)], limit=1)
            #     if sale_order:
            #         sale_amount_total = sale_order.amount_total
            #         milestone_amount = (sale_amount_total * float(percentage))/100
            #         if invocie_amount != milestone_amount:
            #             raise UserError(_('You Can Allow only %s amount')% (milestone_amount))
            move.milestone_id.write({'is_billed':True})
        res = super(AccountInvoice, self).action_post()
        return res



