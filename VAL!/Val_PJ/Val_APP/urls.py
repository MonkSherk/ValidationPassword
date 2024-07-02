from django.urls import path

from Val_APP import views

urlpatterns=[
    path('', views.register, name='index'),
    path('success/', views.success, name='success'),
]