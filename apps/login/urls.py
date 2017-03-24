from django.conf.urls import url
from . import views

# Models --views --TEMPLATES
app_name = "login"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^checkandlogin$', views.checkandlogin, name='check'),
    url(r'^login$', views.login, name='login'),
    url(r'^success$', views.success, name='success'),
    url(r'^logout$', views.logout, name='logout')
]
