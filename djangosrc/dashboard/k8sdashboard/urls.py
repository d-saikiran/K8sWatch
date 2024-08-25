from django.urls import path
from . import views
urlpatterns = [
    path("home/getall",views.show_resources, name="show_resources"),
    path("",views.login, name="login"),
    path("home/", views.kubernetes_resources, name='kubernetes_resources'),
    path("home/<str:namespace>/<str:key>/<str:name>/", views.dynamic_resource_view, name="dynamic_resource"),
    path("home/<str:namespace>/<str:key>/<str:name>/manifest/", views.get_yaml, name="get_yaml"),
    path('home/migrate/', views.migrate_to_cluster, name='migrate_to_cluster'),
    path('home/perform_migration/', views.perform_migration, name='perform_migration'),
]