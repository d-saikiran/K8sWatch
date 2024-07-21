from django.urls import path
from . import views
urlpatterns = [
    path("getall",views.show_resources, name="show_resources"),
    path("", views.kubernetes_resources, name='kubernetes_resources'),
]