from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_page, name='main'),
    url(r'^next_page$', views.post_answer, name='next'),
    url(r'^results_download/dasijadspjda12391213sjdsasiaajdioasdj1232$', views.csv_download, name='results')
]
