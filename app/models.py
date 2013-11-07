#coding: utf-8
import os
import yaml
from django.db import models
from django.contrib import admin


def model_unicode(self):
    return u'Объект с ИД = ' + str(self.id)


def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Создает класс модели.
    """
    class Meta:
        pass

    if app_label:
        setattr(Meta, 'app_label', app_label)

    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    attrs = {'__module__': module, 'Meta': Meta}

    if fields:
        attrs.update(fields)

    model = type(name, (models.Model,), attrs)
    model.__unicode__ = model_unicode
    return model


def get_field_data_type(str_type, verbose_name):
    """
    Возвращаеи Django-тип поля модели по текстовому коду (для 'char', 'int', 'date')
    """
    if str_type == 'char':
        return models.CharField(max_length=100, verbose_name=verbose_name)
    elif str_type == 'int':
        return models.IntegerField(verbose_name=verbose_name)
    elif str_type == 'date':
        return models.DateField(verbose_name=verbose_name)
    else:
        return None


# считываем структуру моделей из YAML файла и создаем их
f = open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r')
yaml_data = f.read()
models_meta = yaml.load(yaml_data)

for k, v in models_meta.iteritems():
    fields = {}
    for field in v['fields']:
        fields[field['id']] = get_field_data_type(field['type'], field['title'])
    model = create_model(
        k,
        app_label='app',
        fields=fields,
        options={'verbose_name': v['title'], 'verbose_name_plural': v['title']}
    )

    # добавляем модель в админку
    admin.site.register(model)
