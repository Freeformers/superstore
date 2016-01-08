from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.DepartmentList.as_view(), name='home'),
]