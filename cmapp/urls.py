from django.conf.urls import url, include
from cmapp import views

urlpatterns = [
    url(r'add_node_type', views.add_node_type),
    url(r'add_new_branch', views.add_new_branch),
    url(r'add_new_business_line', views.add_new_business_line),
    url(r'add_cloud_master', views.add_cloud_master),
    url(r'add_local_master', views.add_local_master),
    url(r'node$', views.node),
    url('add_software_type', views.add_software_type),
    url('add_new_database', views.add_new_database),
    url('add_new_properties', views.add_new_properties),
    url('software', views.software),
    url('properties', views.properties),
    url('add_person_type', views.add_person_type),
    url('person', views.person)
    ]