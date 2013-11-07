#coding: utf-8
import datetime
from django.db.models import get_model
from django.test import TestCase


class ModelTest(TestCase):
    def setUp(self):
        model = get_model(app_label='app', model_name='users')
        self.model = model
        obj = model()
        obj.name = 'Ivan'
        obj.paycheck = 100
        obj.date_joined = '2013-11-07'
        obj.save()

    def test_users_count(self):
        """
        Тестирует количество созданных записей модели
        """
        count = self.model.objects.all().count()
        self.assertEqual(count, 1)

    def test_users_date(self):
        """
        Тестирует правильность задания даты
        """
        obj = self.model.objects.all()[0]
        self.assertEqual(obj.date_joined, datetime.date(2013, 11, 7))
