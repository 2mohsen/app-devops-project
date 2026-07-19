from django.urls import path, include
from devops.blog.apis.products import ProductAPI
urlpatterns = [
    path('product/', ProductAPI.as_view(), name="product"),
]
