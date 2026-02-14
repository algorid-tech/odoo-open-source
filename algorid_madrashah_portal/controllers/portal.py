# -*- encoding: utf-8 -*-
#################################################################
#                                                               #
#       Developed by Algorid Limited                            #
#       Copyright (C) 2026 - Today (https://www.algorid.com)    #
#       Contact us: contact@algorid.com                         #
#                                                               #
#################################################################

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from datetime import datetime, timedelta


class MadrasahPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        # Only compute values if explicitly requested in counters
        # This prevents issues with Odoo 19's JavaScript counter system
        user = request.env.user

        # Get student/guardian for the current user
        student = request.env['algorid.student'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        guardian = request.env['algorid.guardian'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        # Set student/guardian in values for template access
        values['student'] = student if student else False
        values['guardian'] = guardian if guardian else False

        return values

    def _get_student_domain(self):
        """Get domain for student(s) based on current user."""
        user = request.env.user
        student = request.env['algorid.student'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        if student:
            return [('student_id', '=', student.id)]

        guardian = request.env['algorid.guardian'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        if guardian:
            return [('student_id', 'in', guardian.student_ids.ids)]

        return [('id', '=', 0)]  # No access

    @http.route(['/my/students'], type='http', auth='user', website=True)
    def portal_my_students(self, **kw):
        """Portal page showing students (for guardians)."""
        user = request.env.user
        guardian = request.env['algorid.guardian'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        students = guardian.student_ids if guardian else request.env['algorid.student'].sudo().search([
            ('user_id', '=', user.id)
        ])

        values = {
            'students': students,
            'page_name': 'students',
        }
        return request.render('algorid_madrashah_portal.portal_my_students', values)

    @http.route(['/my/student/<int:student_id>'], type='http', auth='user', website=True)
    def portal_student_profile(self, student_id, **kw):
        """View student profile."""
        student = request.env['algorid.student'].sudo().browse(student_id)

        # Check access
        if not self._check_student_access(student):
            return request.redirect('/my')

        values = {
            'student': student,
            'page_name': 'student_profile',
        }
        return request.render('algorid_madrashah_portal.portal_student_profile', values)

    @http.route(['/my/attendance', '/my/attendance/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_attendance(self, page=1, date_begin=None, date_end=None, **kw):
        """Portal page showing attendance records."""
        domain = self._get_student_domain()

        if date_begin:
            domain.append(('date', '>=', date_begin))
        if date_end:
            domain.append(('date', '<=', date_end))

        Attendance = request.env['algorid.student.attendance'].sudo()
        attendance_count = Attendance.search_count(domain)

        pager = portal_pager(
            url='/my/attendance',
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=attendance_count,
            page=page,
            step=20
        )

        attendances = Attendance.search(domain, order='date desc', limit=20, offset=pager['offset'])

        values = {
            'attendances': attendances,
            'page_name': 'attendance',
            'pager': pager,
            'default_url': '/my/attendance',
            'date_begin': date_begin,
            'date_end': date_end,
        }
        return request.render('algorid_madrashah_portal.portal_my_attendance', values)

    @http.route(['/my/fees', '/my/fees/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_fees(self, page=1, **kw):
        """Portal page showing fee status."""
        domain = self._get_student_domain()

        Fee = request.env['algorid.student.fee'].sudo()
        fee_count = Fee.search_count(domain)

        pager = portal_pager(
            url='/my/fees',
            total=fee_count,
            page=page,
            step=20
        )

        fees = Fee.search(domain, order='due_date desc', limit=20, offset=pager['offset'])

        # Calculate totals
        total_due = sum(fees.filtered(lambda f: f.state in ('pending', 'partial')).mapped('due_amount'))

        values = {
            'fees': fees,
            'page_name': 'fees',
            'pager': pager,
            'default_url': '/my/fees',
            'total_due': total_due,
        }
        return request.render('algorid_madrashah_portal.portal_my_fees', values)

    @http.route(['/my/results', '/my/results/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_results(self, page=1, **kw):
        """Portal page showing exam results."""
        domain = self._get_student_domain()
        domain.append(('state', '=', 'published'))

        Result = request.env['algorid.exam.result'].sudo()
        result_count = Result.search_count(domain)

        pager = portal_pager(
            url='/my/results',
            total=result_count,
            page=page,
            step=20
        )

        results = Result.search(domain, order='exam_id desc', limit=20, offset=pager['offset'])

        values = {
            'results': results,
            'page_name': 'results',
            'pager': pager,
            'default_url': '/my/results',
        }
        return request.render('algorid_madrashah_portal.portal_my_results', values)

    @http.route(['/my/result/<int:result_id>'], type='http', auth='user', website=True)
    def portal_result_detail(self, result_id, **kw):
        """View detailed result."""
        result = request.env['algorid.exam.result'].sudo().browse(result_id)

        # Check access
        if not self._check_student_access(result.student_id):
            return request.redirect('/my')

        values = {
            'result': result,
            'page_name': 'result_detail',
        }
        return request.render('algorid_madrashah_portal.portal_result_detail', values)

    @http.route(['/my/timetable'], type='http', auth='user', website=True)
    def portal_my_timetable(self, **kw):
        """Portal page showing class timetable."""
        user = request.env.user
        student = request.env['algorid.student'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        if not student:
            guardian = request.env['algorid.guardian'].sudo().search([
                ('user_id', '=', user.id)
            ], limit=1)
            if guardian and guardian.student_ids:
                student = guardian.student_ids[0]

        timetable = None
        if student:
            timetable = request.env['algorid.timetable'].sudo().search([
                ('class_id', '=', student.class_id.id),
                ('section_id', '=', student.section_id.id),
                ('state', '=', 'active'),
            ], limit=1)

            if not timetable:
                timetable = request.env['algorid.timetable'].sudo().search([
                    ('class_id', '=', student.class_id.id),
                    ('section_id', '=', False),
                    ('state', '=', 'active'),
                ], limit=1)

        periods = request.env['algorid.period'].sudo().search([
            ('period_type', '=', 'class')
        ], order='sequence')

        values = {
            'student': student,
            'timetable': timetable,
            'periods': periods,
            'days': [
                ('0', 'Saturday'),
                ('1', 'Sunday'),
                ('2', 'Monday'),
                ('3', 'Tuesday'),
                ('4', 'Wednesday'),
                ('5', 'Thursday'),
            ],
            'page_name': 'timetable',
        }
        return request.render('algorid_madrashah_portal.portal_my_timetable', values)

    def _check_student_access(self, student):
        """Check if current user has access to this student."""
        user = request.env.user

        if student.user_id and student.user_id.id == user.id:
            return True

        guardian = request.env['algorid.guardian'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)

        if guardian and student.id in guardian.student_ids.ids:
            return True

        return False

