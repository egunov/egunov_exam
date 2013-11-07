from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'add_record/(\w+)/$', 'app.views.add_record'),
    url(r'model_view/(\w+)/$', 'app.views.model_view'),
    url(r'change_field/(\w+)/$', 'app.views.change_field'),
    url(r'$', 'app.views.main'),
)
