# coding: utf-8
from .. import consts
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from division_perm import models
from division_perm.tests.helpers import ListTestMixin, DetailTestMixin


class BaseFuncTest(TestCase):
    view_path = None

    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@soft-way.biz', password='123')
        self.empl = models.Employee.objects.create(user=self.user, last_name='test', first_name='test', middle_name='test')
        func_edit = models.Func.objects.create(code=consts.SYS_EDIT_FUNC, name='test_edit', level=5)
        self.func_read = models.Func.objects.create(code=consts.SYS_READ_FUNC, name='test_read', level=0)
        self.division = models.Division.objects.create(name='Tech Support')
        self.division.employees.add(self.empl)
        role_read = models.Role.objects.create(name='manger', code=self.func_read.code, level=9, division=self.division)
        self.empl.roles.add(role_read)
        self.client.login(username=self.user.username, password='123')

    def get_url(self):
        url = reverse(self.view_path)
        return url


class ListFuncTest(BaseFuncTest, ListTestMixin):
    view_path = 'perm_func_list'
    success_url = reverse('perm_func_list') + '?sort=code'
    model_access = models.Func


class DetailFuncTest(BaseFuncTest, DetailTestMixin):
    view_path = 'perm_func_detail'

    def get_url(self):
        url = reverse(self.view_path, args=[self.func_read.id])
        return url

    def get_instance(self):
        return self.func_read