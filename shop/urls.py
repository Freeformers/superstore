from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.DepartmentList.as_view(), name='home'),
    url(r'^search$', views.ProductSearch.as_view(), name='search'),
    url(r'^create-department$', views.CreateDepartment.as_view(), name='create-department'),
    url(r'^departments/(?P<pk>\d+)$', views.ShopDepartment.as_view(), name='shop-department'),
    url(r'^create-product$', views.CreateProduct.as_view(), name='create-product'),
    url(r'^products/(?P<pk>\d+)$', views.ShopProduct.as_view(), name='shop-product'),
    url(r'^start-purchase$', views.start_purchase, name='start-purchase'),
]