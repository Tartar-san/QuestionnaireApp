from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_page, name='main'),
    url(r'^next_page$', views.answer, name='next'),
]
