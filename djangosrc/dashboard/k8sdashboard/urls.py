from django.urls import path
from . import views
urlpatterns = [
    path("getall",views.show_resources, name="show_resources"),
    path("", views.kubernetes_resources, name='kubernetes_resources'),
    path("<str:namespace>/<str:key>/<str:name>/", views.dynamic_resource_view, name="dynamic_resource"),
    path("<str:namespace>/<str:key>/<str:name>/manifest/", views.get_yaml, name="get_yaml"),
]