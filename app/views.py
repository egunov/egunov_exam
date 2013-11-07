#coding: utf-8
from django.db.models import get_app, get_models, get_model
from django.shortcuts import render_to_response
from app.utils import ok, error


def main(self):
    """
    Выводит начальную страницу сайта.
    """
    app = get_app('app')
    model_list = map(lambda x: {
        'model_name': x._meta.verbose_name_plural,
        'model_classname': x.__name__
    }, get_models(app))
    return render_to_response('base.html', {'model_list': model_list})


def model_view(request, model_name):
    """
    Возвращает json-данные для отображения структуры и данных выбранной в списке модели.
    """
    # определим класс модели
    model = get_model(app_label='app', model_name=model_name)

    meta = map(lambda field: {
        'field_name': field.name,
        'field_type': field.get_internal_type(),
        'field_title': field.verbose_name
    }, model._meta.fields)

    records = []
    for record in model.objects.all():
        d = {}
        for field in meta:
            d[field['field_name']] = record.__dict__[field['field_name']]
        records.append(d)

    res = {
        'model_name': model_name,
        'model_title': model._meta.verbose_name.title(),
        'meta': meta,
        'records': records}
    return ok(res)


def add_record(request, model_name):
    """
    Добавляет новую запись модели.
    """
    # определим класс модели
    model = get_model(app_label='app', model_name=model_name)

    # добавим запись
    try:
        dct = {}
        for k, v in request.POST.iteritems():
            dct[k] = v

        model.objects.create(**dct)
    except Exception as e:
        return error('Ошибка формата' if e.message == '' else e.message)

    return ok({'model_name': model_name})


def change_field(request, model_name):
    """
    Обновляет запись модели.
    Взод:
        POST['field_name_id'] = "имя поля модели,ИД записи"
        POST['new_value'] = "новое значение для записи"
    """
    # определим класс модели
    model = get_model(app_label='app', model_name=model_name)

    # находим нужную запись и обновляем ее значение
    (field_name, record_id) = request.POST['field_name_id'].split(',')
    item = model.objects.get(id=record_id)
    item.__dict__[field_name] = request.POST['new_value']

    try:
        item.save()
    except Exception as e:
        return error('Ошибка формата' if e.message == '' else e.message)

    return ok()
