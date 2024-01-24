from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("upload/", views.upload, name="upload"),
    path("upload-form/", views.upload_form, name="upload-form"),
    path('get_column_names/', views.get_column_names, name='get_column_names'),
    path('daily-return', views.daily_return, name="daily-return"),
    
]
