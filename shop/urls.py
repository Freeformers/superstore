from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.DepartmentList.as_view(), name='home'),
    url(r'^create-department$', views.CreateDepartment.as_view(), name='create-department'),
]