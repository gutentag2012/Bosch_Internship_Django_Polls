from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('polls/<int:poll_id>/', views.single_poll_view, name='poll'),
]