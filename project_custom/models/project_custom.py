# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta
import logging


class ProjectHeader(models.Model):
    _inherit = 'project.project'
    _description = "Personalizacion Header repot"

    @api.model
    def _compute_test_code(self):
        print('Aqui si llego')

class ProjectCustom(models.Model):
    _inherit = 'project.task'
    _description = "Personalizacion APP Project"

    date_start_custom = fields.Date(string='Inicio', index=True, copy=True)
    date_end_custom = fields.Date(string='Logrado', index=True, copy=True)
    status_record_task = fields.Char(compute='_compute_is_record_task')

    test_code = fields.Char(compute='_compute_test_code')

    @api.model
    def _compute_test_code(self):

        print('otra cosa verificando3')


    @api.multi
    def _compute_is_record_task(self):
        #current_date = datetime.date.today().strftime("%d-%m-%Y")
        current_date = datetime.date.today()

        # 1.- Get Domain
        domain_urgente = [
            '&',
            '&', ('tag_ids', '=', 'Urgente'), ('date_deadline', '!=', False),
            ('date_end_custom', '=', False)]
        # 2.- Select record for domain declare domain_urgen
        record_urgente = self.search(domain_urgente)
        # 3.- recore register select

        for task in record_urgente:

            remaining_days = ProjectCustom._valueDate(self, current_date, task.date_deadline, task.name)
            if (remaining_days <= 2) and (remaining_days >= 1):
                #print(remaining_days)
                task.status_record_task = 'warning'
                #print(task.date_deadline - current_date)
            elif (current_date > task.date_deadline) or (remaining_days <= 0):
                task.status_record_task = 'danger'
                #print(task.date_deadline - current_date)
                #Value: datetime.date.today() + datetime.timedelta(days=3)
            # 4.- Select register fech end iqual a Null
            # task.status_record_task = True
            # print(task.date_deadline, " ", task.id, " ", task.status_record_task)

        return True

        # Funtion value day expired caall line 54
    def _valueDate(self, fecha, date_today, name):

        r = relativedelta(date_today, fecha)

        return r.days

    @api.multi
    def _header_report_task(self):
        record_collection = []
        # Do your browse, search, calculations, .. here and then return the data (which you can then use in the QWeb)
        record_collection = self.env['project.project'].search([('name', '=', 'Estrategia de Posicionamiento')])
        return record_collection

    @api.model
    @api.constrains('date_deadline', 'tag_ids')
    def _check_tags_urgente(self, *args, **kwargs):

        list_tags = []
        for record in self.tag_ids:
            list_tags.append(record.name)

        if self.date_deadline != False:
            if 'Urgente' not in list_tags:
                raise ValidationError('Debe colocar Etiqueta URGENTE')
            else:
                pass
                #print('SI esta la etiqueta Urg')
        else:
            if 'Urgente' in list_tags:
                raise ValidationError('Debe colocar FECHA LÍMITE')

        # print(list_tags)

class ProjectViewTree(models.Model):
    _name = 'project.view_extend_tree'
    _inherit = 'project.task'
    _description = "View Tree Extend"


