from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_initial_page, name='initial_page'),
    url(r'^question$', views.get_page, name='main'),
    url(r'^next_page$', views.post_answer, name='next'),
]
