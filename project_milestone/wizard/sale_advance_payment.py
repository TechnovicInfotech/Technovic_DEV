# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    milestone_id = fields.Many2one('project.milestone', string="Milestone")

    @api.onchange('milestone_id')
    def onchange_medium_id(self):
        domain = [('id','in',[])]
        if self._context.get('active_model') == 'sale.order' and self._context.get('active_id', False):
            sale_order = self.env['sale.order'].browse(self._context.get('active_id'))
            project_id = sale_order.project_id
            if project_id and project_id.project_milestone_ids:
                project_milestone_ids = project_id.project_milestone_ids.ids
                if sale_order.milestone_ids:
                    sale_milestone_ids = sale_order.milestone_ids.ids
                    milestone_lst = list(set(project_milestone_ids) - set(sale_milestone_ids))
                    domain = [('id','in',milestone_lst)]
                else:
                    domain = [('id','in',project_milestone_ids)]
        return {'domain':{'milestone_id':domain}}

    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if sale_orders and sale_orders.project_id:
            project_milestone_ids = sale_orders.project_id.project_milestone_ids.ids
            sale_milestone_ids = sale_orders.milestone_ids.ids
            if len(project_milestone_ids) != len(sale_milestone_ids) and not self.milestone_id:
                raise UserError(_('Please Select Milestone First !'))
            if self.milestone_id:
                sale_milestone_ids.append(self.milestone_id.id)
                sale_orders.write({'latest_milestone_id': self.milestone_id.id,'milestone_ids':[(6,False,sale_milestone_ids)]})

        res = super(SaleAdvancePaymentInv,self).create_invoices()
        return res
