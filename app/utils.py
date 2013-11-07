#coding: utf-8
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder


def ok(data=None):
    response = {'success': True}
    if data:
        response.update(data)
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
                        mimetype='application/json')


def error(msg):
    response = {'msg': msg, 'success': False}
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
                        mimetype='application/json')
