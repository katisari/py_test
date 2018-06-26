from django.conf.urls import url
from . import views       
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^addJob$', views.add_job, name="add_job"),
    url(r'^process_add$', views.process_add, name="process_add"),
    url(r'^view/(?P<id>\d+)$', views.view_job, name="view_job"),
    url(r'^edit/(?P<id>\d+)$', views.edit_job, name="edit_job"),
    url(r'^process_edit/(?P<id>\d+)$', views.process_edit, name="process_edit"),
    url(r'^cancel/(?P<id>\d+)$', views.cancel, name="cancel"),
    url(r'^add_to_myjobs/(?P<id>\d+)$', views.add_myjobs, name="add_myjobs"),
    url(r'^logout$', views.logoff, name="logoff")
]                          