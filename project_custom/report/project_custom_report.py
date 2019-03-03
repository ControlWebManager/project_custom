# -*- coding: utf-8 -*-

import logging
from odoo import tools
from odoo import api, fields, models
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

#https://www.cybrosys.com/blog/qweb-reports-in-odoo12
#https://gist.github.com/CakJuice/e42eef6910a8268352e763118d21df19

class ProjectCustomReport(models.AbstractModel):
    _name = 'report.project_custom.header_task_layout'
    _description = "Custom proyecto reporte NUEVo"

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('project_custom.header_task_layout')
        print('aqui aparezco')

        #1.- project Name
        projects = self.env['project.project'].search([])
        #----------------
        #2.- Count task for Project
        task_projects = self.env['project.task']

        project_task_count = {}
        group_info = {}

        for rec in projects:

            group_asigne = []
            group_info = {}
        # 2.- Count task for Project

            task_count_project = task_projects.search_count([('project_id', 'in', rec.ids)])

        # 3.- Empleados asignados por Proyecto

            employes_asigne = task_projects.read_group(
                domain=[('project_id', 'in', rec.ids)],
                fields=['user_id'], groupby=['user_id']
            )
            employe_asigne = dict((data['user_id'][1], data['user_id_count']) for data in employes_asigne)

            for k, v in employe_asigne.items():
                group_asigne.append(k)

            group_info = {
                'project': rec.name,
                'asigne': group_asigne,
                'task_count': task_count_project,
            }

            print(group_info)

        # ----------------
        #5.- Employe Work in Projects

        task_active_id = self.env['project.task'].search([('active', '=', True)])

        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
        }

    @api.noguess
    def report_action(self, docids, data=None, config=True):
        """Return an action of type ir.actions.report.

        :param docids: id/ids/browserecord of the records to print (if not used, pass an empty list)
        :param report_name: Name of the template to generate an action for
        """

        context = self.env.context
        if docids:
            if isinstance(docids, models.Model):
                active_ids = docids.ids
            elif isinstance(docids, int):
                active_ids = [docids]
            elif isinstance(docids, list):
                active_ids = docids
            context = dict(self.env.context, active_ids=active_ids)

        return {
            'context': context,
            'data': data,
            'type': 'ir.actions.report',
            'report_name': self.report_name,
            'report_type': self.report_type,
            'report_file': self.report_file,
            'name': self.name,
        }